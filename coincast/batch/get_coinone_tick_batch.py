
from coincast import database
from coincast.model.coinone_tick import CoinoneTick
from coincast.api import coinone_api

db_url = 'mysql://dev:qkrwnsdn92!@localhost/testdb?charset=utf8'
database.DBManager.init(db_url)
database.DBManager.init_db()

dao = database.dao
queries = dao.query(CoinoneTick)
entries = [dict(currency=q.currency, timestamp=q.timestamp, last=q.last) for q in queries]

ticks_dict = coinone_api.get_ticks_for()
ticks_list = coinone_api.coinone_tick.api2orm_list(ticks_dict)

dao.add_all(ticks_list)
dao.commit()

queries = dao.query(CoinoneTick)
entries = [dict(currency=q.currency, timestamp=q.timestamp, last=q.last) for q in queries]

print(entries[:10])