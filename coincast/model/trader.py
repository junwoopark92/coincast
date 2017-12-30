from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, TIMESTAMP, JSON
from coincast.model import Base
from time import localtime, strftime


class Trader(Base):
    __tablename__ = 'trader_status'

    trader_no = Column(Integer, primary_key=True)
    type = Column(String(20))  # ml, statics
    name = Column(String(30))
    comment = Column(String(200))

    trader_parm = Column(JSON(200))

    use_yn = Column(String(10))

    create_dt = Column(DateTime, unique=False)
    update_dt = Column(DateTime, unique=False)

    def __init__(self, trader_no, _type, name, comment, trader_parm, use_yn):
        self.trader_no = trader_no
        self.type = _type
        self.name = name
        self.comment = comment
        self.trader_parm = trader_parm
        self.use_yn = use_yn

        self.create_dt = strftime('%Y/%m/%d %H:%M:%S', localtime())
        self.update_df = self.create_dt


if __name__ == '__main__':
    from coincast.database import DBManager

    db_url = 'mysql://DEV:coincast@49.142.50.199/CC_DEV?charset=utf8'
    DBManager.init(db_url)
    DBManager.init_db()

    from coincast.database import dao
    queries = dao.query(Trader)
    entries = [dict(trader_no=q.trader_no, type=q.type, name=q.name, parm=q.trader_parm) for q in queries]

    trader = Trader(trader_no=2, _type='statics', name='Test-Trader-01', comment='test-version',
                    trader_parm={"in_seq": 14, "time": "3600", "target-rate": 5, "lower-bound-rsi": 30}, use_yn='Y')

    dao.add(trader)
    # Trader.query.filter_by(trader_no=1).delete()
    dao.commit()
    #
    # queries = dao.query(Trader)
    # entries = [dict(trader_no=q.trader_no, type=q.type, name=q.name, trader_parm=q.trader_parm) for q in queries]

    print(entries[:10])
