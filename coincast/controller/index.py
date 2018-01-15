# -*- coding: utf-8 -*-
from coincast.coincast_blueprint import coincast
from coincast import socketio
from flask import redirect, url_for, render_template, request
from flask_socketio import send
from coincast.database import dao
from coincast.model.coinone_tick import CoinoneTick
from coincast.model.trader import Trader
from coincast.model.trader_run_hist import SimulTraderRunHist
from coincast.model.trader_order import SimulTraderOrder
from coincast import thread_manager
from coincast.coincast_logger import Log
from coincast.validation import is_positive_number


import json
from sqlalchemy import func
import numpy as np
from datetime import datetime, timedelta
from time import localtime, strftime
import eventlet

from coincast.bot.server_push import rsi_trader_alarm, enrollment_trader
from coincast.bot import RUNNING_TRADER


@coincast.teardown_request
def shutdown_session(exception=None):
    dao.remove()


@coincast.route('/')
def index():
    """로그인이 성공한 다음에 보여줄 초기 페이지"""
    return render_template('home.html')


@coincast.route('/forecaster')
def show_forecasters():
    return render_template('forecasters.html')


@coincast.route('/traders')
def show_traders():
    trader_list = dao.query(SimulTraderRunHist, Trader)\
        .filter(SimulTraderRunHist.end_dt.is_(None))\
        .filter(Trader.trader_no == SimulTraderRunHist.trader_no)\
        .all()

    is_alive = dict()
    for run_no in RUNNING_TRADER.keys():
        is_alive[run_no] = True

    return render_template('traders.html', trader_list=trader_list, is_alive=is_alive)


@coincast.route('/traders/order', methods=['post'])
def show_trader_order_hist():
    data = request.json
    Log.info(data)

    orders = dao.query(SimulTraderOrder)\
        .filter(SimulTraderOrder.run_no == data['run_no'])\
        .order_by(SimulTraderOrder.create_dt.desc())\
        .all()

    orders = [order.__dict__ for order in orders]

    order_list = []
    for order in orders:
        order.pop('_sa_instance_state')
        order.pop('update_dt')
        order['create_dt'] = order['create_dt'].strftime('%Y/%m/%d %H:%M:%S')
        order_list.append(order)

    return json.dumps({'status': 'OK', 'order_list': order_list})


@coincast.route('/create/simul')
def show_create_trader_page():
    # trader list 가져오기
    trader_list = dao.query(Trader.name).filter(Trader.use_yn == 'Y').all()
    coin_list = dao.query(CoinoneTick.currency).group_by(CoinoneTick.currency).all()
    return render_template('trader_create.html', trader_list=trader_list, coin_list=coin_list)


@coincast.route('/create/trader', methods=['POST'])
def create_trader():
    try:
        data = request.form.to_dict()
        Log.info(data)
        trader_name = data.pop('trader')
        interval = is_positive_number(int(data.pop('interval')))
        balance = is_positive_number(int(data.pop('balance')))
        currency = data.pop('currency')
        trader_parm = data
    except Exception as e:
        Log.info(e)
        return redirect(url_for('.show_create_trader_page'))

    trader_no = dao.query(Trader.trader_no).filter(Trader.name == trader_name).all()[0][0]

    # run_no: auto_increment
    dao.add(SimulTraderRunHist(trader_no=trader_no, currency=currency,
                               time_interval=interval, init_balance=balance, trader_parm=trader_parm))
    dao.commit()

    return redirect(url_for('.show_traders'))


@coincast.route('/create/trader/parm', methods=['post'])
def get_parm_list():
    trader = request.json
    trader_parm = dao.query(Trader.trader_parm).filter(Trader.name == trader['trader']).first()

    return json.dumps({'status': 'OK', 'trader_parm': trader_parm})


@coincast.route('/traders/seq', methods=['post'])
def get_seq():
    run_hist = request.json
    Log.info(run_hist)

    show_time_unit = '%Y,%m,%d'

    yesterday = datetime.now()

    tick_data = dao.query(func.date_format(CoinoneTick.create_dt, '%Y,%m,%d,%H'), func.avg(CoinoneTick.last)) \
        .filter_by(currency=run_hist['currency']) \
        .filter(func.date_format(CoinoneTick.create_dt, '%Y,%m,%d,%H') >= yesterday.strftime(show_time_unit))\
        .group_by(func.date_format(CoinoneTick.create_dt, '%Y,%m,%d,%H')) \
        .order_by(func.date_format(CoinoneTick.create_dt, '%Y,%m,%d,%H').asc()) \
        .limit(24).all()

    Log.debug(tick_data)
    tick_list = [(time.split(','), float(tick)) for (time, tick) in tick_data]
    tick_last = [float(tick) for time, tick in tick_data]

    y_max = round(np.max(tick_last)) + round(np.max(tick_last)*0.1)
    y_min = round(np.min(tick_last)) - round(np.min(tick_last)*0.1)

    return json.dumps({'status': 'OK', 'currency': run_hist['currency'], 'ticks': tick_list, 'max': y_max, 'min': y_min})


@coincast.route('/traders/run', methods=['post'])
def run_trader():
    data = request.json
    Log.info(data)
    # start trader
    start_dt = strftime('%Y/%m/%d %H:%M:%S', localtime())
    Log.debug(start_dt)

    interval = dao.query(SimulTraderRunHist.time_interval).filter(SimulTraderRunHist.run_no == data['run_no']).first()[0]

    g = eventlet.spawn(enrollment_trader, rsi_trader_alarm, data['run_no'], interval)
    RUNNING_TRADER[data['run_no']] = g

    # update
    dao.query(SimulTraderRunHist.start_dt) \
        .filter(SimulTraderRunHist.run_no == data['run_no']) \
        .update({SimulTraderRunHist.start_dt: start_dt})
    dao.commit()

    return json.dumps({'status': 'OK', 'start_dt': start_dt})


@coincast.route('/traders/stop', methods=['post'])
def stop_trader():
    data = request.json
    Log.info(data)
    end_dt = strftime('%Y/%m/%d %H:%M:%S', localtime())

    g = RUNNING_TRADER.pop(data['run_no'])
    g.kill()

    # update
    dao.query(SimulTraderRunHist.end_dt)\
        .filter(SimulTraderRunHist.run_no == data['run_no'])\
        .update({SimulTraderRunHist.end_dt: end_dt})
    dao.commit()

    return json.dumps({'status': 'OK', 'end_dt': end_dt})

