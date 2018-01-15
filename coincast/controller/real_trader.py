# -*- coding: utf-8 -*-
from coincast.coincast_blueprint import coincast
from coincast import socketio
from flask import redirect, url_for, render_template, request
from flask_socketio import send
from coincast.database import dao
from coincast.model.coinone_tick import CoinoneTick
from coincast.model.trader import Trader
from coincast.model.trader_run_hist import RealTraderRunHist
from coincast import thread_manager
from coincast.coincast_logger import Log
from coincast.validation import is_positive_number

import json
from sqlalchemy import func
import numpy as np
from datetime import datetime, timedelta
from time import localtime, strftime
import eventlet

from coincast.bot.server_push import real_rsi_trader_alarm ,enrollment_trader
from coincast.bot import RUNNING_REAL_TRADER

@coincast.route('/trader/real')
def show_real_traders():
    trader_list = dao.query(RealTraderRunHist, Trader) \
        .filter(RealTraderRunHist.end_dt.is_(None)) \
        .filter(Trader.trader_no == RealTraderRunHist.trader_no) \
        .all()

    is_alive = dict()
    for run_no in RUNNING_REAL_TRADER.keys():
        is_alive[run_no] = True

    return render_template('real_traders.html', trader_list=trader_list, is_alive=is_alive)

@coincast.route('/create/real')
def show_create_real_trader_page():
    # trader list 가져오기
    trader_list = dao.query(Trader.name).filter(Trader.use_yn == 'Y').all()
    coin_list = dao.query(CoinoneTick.currency).group_by(CoinoneTick.currency).all()
    return render_template('real_trader_create.html', trader_list=trader_list, coin_list=coin_list)

@coincast.route('/create/real/trader', methods=['POST'])
def create_real_trader():
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
        return redirect(url_for('.show_create_real_trader_page'))

    trader_no = dao.query(Trader.trader_no).filter(Trader.name == trader_name).all()[0][0]

    # run_no: auto_increment
    dao.add(RealTraderRunHist(trader_no=trader_no, currency=currency,
                               time_interval=interval, init_balance=balance, trader_parm=trader_parm))
    dao.commit()

    return redirect(url_for('.show_real_traders'))

@coincast.route('/traders/real/run', methods=['post'])
def run_real_trader():
    data = request.json
    Log.info(data)
    # start trader
    start_dt = strftime('%Y/%m/%d %H:%M:%S', localtime())
    Log.debug(start_dt)

    interval = dao.query(RealTraderRunHist.time_interval).filter(RealTraderRunHist.run_no == data['run_no']).first()[0]

    g = eventlet.spawn(enrollment_trader, real_rsi_trader_alarm, data['run_no'], interval)
    RUNNING_REAL_TRADER[data['run_no']] = g

    # update
    dao.query(RealTraderRunHist.start_dt) \
        .filter(RealTraderRunHist.run_no == data['run_no']) \
        .update({RealTraderRunHist.start_dt: start_dt})
    dao.commit()

    return json.dumps({'status': 'OK', 'start_dt': start_dt})

@coincast.route('/traders/real/stop', methods=['post'])
def stop_real_trader():
    data = request.json
    Log.info(data)
    end_dt = strftime('%Y/%m/%d %H:%M:%S', localtime())

    g = RUNNING_REAL_TRADER.pop(data['run_no'])
    g.kill()

    # update
    dao.query(RealTraderRunHist.end_dt)\
        .filter(RealTraderRunHist.run_no == data['run_no'])\
        .update({RealTraderRunHist.end_dt: end_dt})
    dao.commit()

    return json.dumps({'status': 'OK', 'end_dt': end_dt})