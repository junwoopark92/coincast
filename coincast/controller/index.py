# -*- coding: utf-8 -*-
from coincast.coincast_blueprint import coincast
from coincast import socketio
from flask import redirect, url_for, render_template, request
from flask_socketio import send
from coincast.database import dao
from coincast.model.coinone_tick import CoinoneTick
from coincast.model.trader import Trader
from coincast.model.trader_run_hist import SimulTraderRunHist
from coincast import thread_manager
from coincast.coincast_logger import Log
from coincast.validation import is_positive_number


import json
from sqlalchemy import func
import numpy as np
from datetime import datetime, timedelta
from time import localtime, strftime


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
    Log.info(trader_list[0][0].end_dt)
    return render_template('traders.html', trader_list=trader_list)


@coincast.route('/create')
def show_create_trader_page():
    # trader list 가져오기
    trader_list = dao.query(Trader.name).filter(Trader.use_yn == 'Y').all()
    coin_list = dao.query(CoinoneTick.currency).group_by(CoinoneTick.currency).all()
    return render_template('trader_create.html', trader_list=trader_list, coin_list=coin_list)


@coincast.route('/create/trader', methods=['POST'])
def create_trader():
    try:
        trader_name = request.form['trader']
        interval = is_positive_number(int(request.form['interval']))
        balance = is_positive_number(int(request.form['balance']))
        currency = request.form['currency']
    except Exception as e:
        Log.info(e)
        return redirect(url_for('.show_create_trader_page'))

    Log.debug(trader_name+str(interval)+str(balance))

    trader_no = dao.query(Trader.trader_no).filter(Trader.name == trader_name).all()[0][0]

    # run_no: auto_increment
    dao.add(SimulTraderRunHist(trader_no=trader_no, currency=currency, time_interval=interval, init_balance=balance))
    dao.commit()

    return redirect(url_for('.show_traders'))


@coincast.route('/traders/seq', methods=['post'])
def get_seq():
    run_hist = request.json
    Log.info(run_hist)

    yesterday = datetime.now()

    tick_data = dao.query(func.date_format(CoinoneTick.create_dt, '%Y,%m,%d,%H'), func.avg(CoinoneTick.last)) \
        .filter_by(currency=run_hist['currency']) \
        .filter(func.date_format(CoinoneTick.create_dt, '%Y,%m,%d,%H') >= yesterday.strftime('%Y,%m,%d'))\
        .group_by(func.date_format(CoinoneTick.create_dt, '%Y,%m,%d,%H')) \
        .order_by(func.date_format(CoinoneTick.create_dt, '%Y,%m,%d,%H').asc()) \
        .limit(24).all()

    print(tick_data)
    tick_list = [(time.split(','), float(tick)) for (time, tick) in tick_data]
    tick_last = [float(tick) for time, tick in tick_data]

    y_max = round(np.max(tick_last)) + round(np.max(tick_last)*0.1)
    y_min = round(np.min(tick_last)) - round(np.min(tick_last)*0.1)

    return json.dumps({'status': 'OK','currency': run_hist['currency'],'ticks': tick_list, 'max': y_max, 'min': y_min})


@coincast.route('/traders/run', methods=['post'])
def run_trader():
    data = request.json
    Log.info(data)
    # start trader
    start_dt = strftime('%Y/%m/%d %H:%M:%S', localtime())
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
    # update
    dao.query(SimulTraderRunHist.end_dt)\
        .filter(SimulTraderRunHist.run_no == data['run_no'])\
        .update({SimulTraderRunHist.end_dt: end_dt})
    dao.commit()
    return json.dumps({'status': 'OK', 'end_dt': end_dt})

