from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, TIMESTAMP, JSON
from coincast.model import Base

from time import localtime, strftime


class SimulTraderOrder(Base):
    __tablename__ = 'simul_trader_order_hist'
    order_no = Column(Integer, primary_key=True)
    run_no = Column(Integer, primary_key=True)
    type = Column(String)

    price = Column(Integer)
    volume = Column(Integer)

    success_yn = String(String(10))

    create_dt = Column(DateTime, unique=False)
    update_dt = Column(DateTime, unique=False)

    def __init__(self, order_no, run_no, _type, price, volume):
        self.order_no = order_no
        self.run_no = run_no
        self.type = _type
        self.price = price
        self.volume = volume
        self.success_yn = 'Y'

        self.create_dt = strftime('%Y/%m/%d %H:%M:%S', localtime())
        self.update_dt = self.create_dt


class RealTraderOrder(Base):
    __tablename__ = 'real_trader_order_hist'
    pass
