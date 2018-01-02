from coincast.model.coinone_tick import CoinoneTick
from coincast.model.trader_order import SimulTraderOrder
from coincast.model.trader_run_hist import SimulTraderRunHist
from coincast.model.trader import Trader
from datetime import datetime, timedelta

from coincast.coincast_logger import Log
from sqlalchemy.sql import func
import pandas as pd
from time import localtime


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


def get_rsi(seq):
    diff_prev = seq.shift(1) - seq
    AU = diff_prev[diff_prev > 0].sum()
    AD = -diff_prev[diff_prev <= 0].sum()
    RSI = round(AU / (AU + AD) * 100, 2)
    return RSI


class rsi_trader_v01():
    time_unit = 15
    bot_dao = None
    run_info = None
    trader_parm = None

    def __init__(self, _dao, run_info):
        self.run_info = run_info
        self.bot_dao = _dao
        self.trader_parm = run_info.trader_parm
        self.time_unit = int(self.trader_parm['time_unit_min'])

    def get_indexes(self, currency):
        current_price = self.bot_dao.query(CoinoneTick.last) \
            .filter(CoinoneTick.currency == currency) \
            .order_by(CoinoneTick.create_dt.desc()) \
            .first()[0]

        yesterday = datetime.now() - timedelta(hours=24)

        period = int(self.trader_parm['period'])

        time = [i*self.time_unit for i in range(int(60 / self.time_unit))]

        data = self.bot_dao.query(CoinoneTick.create_dt, CoinoneTick.last) \
            .filter_by(currency=currency) \
            .filter(func.date_format(CoinoneTick.create_dt, '%Y,%m,%d,%H') >= yesterday.strftime('%Y,%m,%d')) \
            .filter(func.Minute(CoinoneTick.create_dt).in_(time)) \
            .filter(func.Second(CoinoneTick.create_dt) < 5) \
            .order_by(CoinoneTick.create_dt.desc()) \
            .limit(period-1) \
            .all()

        Log.debug(data)

        if len(data) != period-1:
            print(len(data), period)
            return None, current_price

        seq = [float(last) for time, last in data]
        seq.insert(0, current_price)

        rsi = get_rsi(pd.Series(seq))

        return rsi, current_price

    def buy(self):
        rsi, buy_price = self.get_indexes(currency=self.run_info.currency)
        volume = int(self.run_info.cur_balance / buy_price)

        if volume < 1:
            return None, None, rsi

        if rsi is None:
            return None, None, rsi

        if rsi < float(self.run_info.trader_parm['lower-bound-rsi']):
            order = SimulTraderOrder(self.run_info.run_no, 'buy', buy_price, volume)
            self.bot_dao.add(order)
            balance = self.run_info.cur_balance - buy_price*volume

            self.bot_dao.query(SimulTraderRunHist) \
                .filter(SimulTraderRunHist.run_no == self.run_info.run_no) \
                .update({SimulTraderRunHist.cur_balance: balance,
                         SimulTraderRunHist.num_of_order: SimulTraderRunHist.num_of_order + 1})
            self.bot_dao.commit()

            return buy_price, volume, rsi

        return None, None, rsi

    def sell(self):
        last_order = self.bot_dao.query(SimulTraderOrder)\
            .filter(SimulTraderOrder.run_no == self.run_info.run_no)\
            .order_by(SimulTraderOrder.order_no.desc())\
            .first()

        # none order
        if last_order is None:
            return None, -1

        # none remain buy order
        if last_order.type == 'sell':
            return None, -2

        # get current rsi and price
        rsi, sell_price = self.get_indexes(currency=self.run_info.currency)
        revenue_rate = (sell_price - last_order.price)/last_order.price*100

        # update current balance
        balance = self.run_info.cur_balance + sell_price * last_order.volume

        self.bot_dao.query(SimulTraderRunHist) \
            .filter(SimulTraderRunHist.run_no == self.run_info.run_no) \
            .update({SimulTraderRunHist.cur_balance: balance})
        
        if revenue_rate > float(self.run_info.trader_parm['target-rate']):
            order = SimulTraderOrder(self.run_info.run_no, 'sell', sell_price, last_order.volume)
            self.bot_dao.add(order)

            self.bot_dao.query(SimulTraderRunHist) \
                .filter(SimulTraderRunHist.run_no == self.run_info.run_no) \
                .update({SimulTraderRunHist.num_of_order: SimulTraderRunHist.num_of_order + 1})

            self.bot_dao.commit()

            return sell_price, round(revenue_rate, 2)

        return None, round(revenue_rate, 2)


if __name__ == '__main__':
    pass