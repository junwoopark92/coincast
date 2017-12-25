from coincast.database import dao
from coincast import socketio
from coincast.model.coinone_tick import CoinoneTick
from coincast.coincast_logger import Log

import sys
import eventlet
import time


def listen(func, interval=10):
    while True:
        func()
        if interval != 0:
            time.sleep(interval)


def update_last_tick(currency='btc'):
    queries = dao.query(CoinoneTick)
    tick = queries.filter_by(currency=currency).order_by(CoinoneTick.timestamp.desc()).first()

    tick_dict = dict()
    tick_dict['create_dt'] = tick.create_dt.strftime("%Y-%m-%d %H:%M:%S")
    tick_dict['currency'] = tick.currency
    tick_dict['last'] = tick.last
    tick_dict['rise_fall_rate'] = round(((tick.last - tick.yesterday_last)/tick.yesterday_last)*100, 2)

    Log.info(tick_dict)

    socketio.emit('message', tick_dict, broadcast=True, namespace='/tick')
    eventlet.sleep(0)
    dao.remove()