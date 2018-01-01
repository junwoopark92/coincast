from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, TIMESTAMP, JSON
from coincast.model import Base

from time import localtime, strftime


class SimulTraderOrder(Base):
    __tablename__ = 'simul_trader_order_hist'

    order_no = Column(Integer, primary_key=True)
    run_no = Column(Integer)
    type = Column(String(10))

    price = Column(Integer)
    volume = Column(Integer)

    success_yn = Column(String(10))

    create_dt = Column(DateTime, unique=False)
    update_dt = Column(DateTime, unique=False)

    def __init__(self, run_no, _type, price, volume):
        self.run_no = run_no
        self.type = _type
        self.price = price
        self.volume = volume
        self.success_yn = 'Y'

        self.create_dt = strftime('%Y/%m/%d %H:%M:%S', localtime())
        self.update_dt = self.create_dt


# class RealTraderOrder(Base):
#     __tablename__ = 'real_trader_order_hist'
#     pass



if __name__ == '__main__':
    from coincast.database import DBManager

    db_url = 'mysql://REAL:coincast@49.142.50.199/CC_REAL?charset=utf8'
    DBManager.init(db_url)
    DBManager.init_db()

    from coincast.database import dao

    queries = dao.query(SimulTraderOrder)
    entries = [dict(order_no=q.order_no, run_no=q.run_no,type=q.type) for q in queries]
    dao.commit()

    print(entries[:10])