from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError


dao = None

class DBManager:
    """데이터베이스 처리를 담당하는 공통 클래스"""

    __engine = None
    __session = None

    @staticmethod
    def init(db_url, db_log_flag=False):
        DBManager.__engine = create_engine(db_url, echo=db_log_flag, pool_recycle=False)
        DBManager.__session = \
            scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=DBManager.__engine))

        global dao
        dao = DBManager.__session
        #print(type(dao))

    @staticmethod
    def init_db():
        from coincast.model import Base
        Base.metadata.create_all(bind=DBManager.__engine)
        Base.query = dao.query_property()





import time
if __name__ == '__main__':

    from coincast.model.coinone_tick import CoinoneTick
    from coincast.api import coinone_api

    db_url = 'mysql://dev:coincast@localhost/testdb?charset=utf8'
    DBManager.init(db_url)
    DBManager.init_db()

    queries = dao.query(CoinoneTick)
    entries = [dict(currency=q.currency, timestamp=q.timestamp, last=q.last) for q in queries]

    ticks_dict = coinone_api.get_ticks_for()
    ticks_list = coinone_api.coinone_tick.api2orm_list(ticks_dict)

    dao.add_all(ticks_list)
    dao.commit()

    queries = dao.query(CoinoneTick)
    entries = [dict(currency=q.currency, timestamp=q.timestamp, last=q.last) for q in queries]

    print(entries[:10])


