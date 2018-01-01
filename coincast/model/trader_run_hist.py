from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, TIMESTAMP, JSON
from coincast.model import Base

from time import localtime, strftime


class SimulTraderRunHist(Base):
    __tablename__ = 'simul_trader_run_hist'

    run_no = Column(Integer, primary_key=True)

    trader_no = Column(Integer)
    time_interval = Column(Integer)
    currency = Column(String(10))
    init_balance = Column(Integer)

    cur_balance = Column(Integer)
    all_revenue_rate = Column(Float)
    num_of_order = Column(Integer)

    trader_parm = Column(JSON(200))

    start_dt = Column(DateTime, unique=False)
    end_dt = Column(DateTime, unique=False)

    create_dt = Column(DateTime, unique=False)
    update_dt = Column(DateTime, unique=False)

    def __init__(self, trader_no, currency, init_balance, time_interval, trader_parm):
        self.trader_no = trader_no
        self.currency = currency
        self.cur_balance = init_balance
        self.init_balance = init_balance
        self.time_interval = time_interval
        self.trader_parm = trader_parm

        self.num_of_order = 0
        self.revenue_rate = 0

        self.create_dt = strftime('%Y/%m/%d %H:%M:%S', localtime())
        self.update_dt = self.create_dt


# class RealTraderRunHist(Base):
#     __tablename__ = 'real_trader_run_hist'
#
#     run_no = Column(Integer, primary_key=True)
#     trader_no = Column(Integer)
#
#     cur_balance = Column(Integer)
#     init_balance = Column(Integer)
#     revenue_rate = Column(Float)
#
#     num_of_order = Column(Integer)
#
#     invoke_interval = Column(Integer)
#
#     start_dt = Column(DateTime, unique=False)
#     end_dt = Column(DateTime, unique=False)
#
#     create_dt = Column(DateTime, unique=False)
#     update_dt = Column(DateTime, unique=False)
#
#     def __init__(self, trader_no, init_balance, invoke_interval):
#         self.trader_no = trader_no
#         self.cur_balance = init_balance
#         self.init_balance = init_balance
#         self.invoke_interval = invoke_interval
#
#         self.num_of_order = 0
#         self.revenue_rate = 0
#
#         self.create_dt = strftime('%Y/%m/%d %H:%M:%S', localtime())
#         self.update_dt = self.create_dt


if __name__ == '__main__':
    from coincast.database import DBManager

    db_url = 'mysql://REAL:coincast@49.142.50.199/CC_REAL?charset=utf8'
    DBManager.init(db_url)
    DBManager.init_db()

    from coincast.database import dao

    queries = dao.query(SimulTraderRunHist)
    entries = [dict(trader_no=q.trader_no, run_no=q.run_no, interval=q.time_interval) for q in queries]
    dao.commit()

    print(entries[:10])

