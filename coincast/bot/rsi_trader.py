from coincast.model.coinone_tick import CoinoneTick

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
    diff_prev = seq - seq.shift(1)
    AU = diff_prev[diff_prev > 0].mean()
    AD = -diff_prev[diff_prev <= 0].mean()
    RSI = round(AU / (AU + AD) * 100, 2)
    return RSI


class rsi_trader_v01(metaclass=Singleton):
    balance = None
    rsi_prev = 15
    time_unit = '%Y-%m-%d %H'
    bot_dao = None
    position = None
    create_dt = None

    def __init__(self, _dao, balance, rsi_prev, time_unit):
        self.balance = balance
        self.rsi_prev = rsi_prev
        self.time_unit = time_unit
        self.bot_dao = _dao
        self.create_dt = localtime()

    def get_indexes(self, currency):
        data = self.bot_dao.query(func.date_format(CoinoneTick.create_dt, self.time_unit), func.avg(CoinoneTick.last)) \
            .filter(CoinoneTick.currency == currency) \
            .group_by(func.date_format(CoinoneTick.create_dt, self.time_unit)) \
            .order_by(func.date_format(CoinoneTick.create_dt, self.time_unit).desc()) \
            .limit(14) \
            .all()

        df = pd.DataFrame(data, columns=['date', 'last']).set_index('date')
        df['last'] = df['last'].astype(float)
        seq = df['last']
        rsi = get_rsi(seq)

        current_price = self.bot_dao.query(CoinoneTick.last)\
            .filter(CoinoneTick.currency == currency)\
            .order_by(CoinoneTick.create_dt.desc())\
            .first()[0]

        return rsi, current_price

    def buy(self):
        if self.position is not None:
            return None

        rsi, buy_price = self.get_indexes(currency='xrp')

        if rsi < 30:
            self.position = buy_price
            return buy_price

    def sell(self):
        if self.position is None:
            return None

        rsi, sell_price = self.get_indexes(currency='xrp')

        revenue_rate = (sell_price - self.position)/self.position*100
        if revenue_rate > 10:
            self.position = None
            return sell_price


if __name__ == '__main__':
    pass