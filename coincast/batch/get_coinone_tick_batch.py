import sys

from configparser import ConfigParser
from sqlalchemy import func

from coincast import database
from coincast.model.coinone_tick import CoinoneTick
from coincast.api import coinone_api
from coincast import util


def main():
    logger = util.get_logger("get_coinone_tick_batch")
    logger.setLevel(util.logging.INFO)

    _ = sys.argv[0]
    section = sys.argv[1]

    config = ConfigParser()
    config.read('batch.conf')
    db_url = config.get(section, 'db_url')
    logger.info("batch.conf section: " + section)
    logger.info("batch.conf db_url: "+db_url)

    database.DBManager.init(db_url)
    database.DBManager.init_db()

    dao = database.dao
    before_cnt = dao.query(func.count(CoinoneTick.timestamp)).all()[0][0]
    logger.info('after count: '+str(before_cnt))

    ticks_dict = coinone_api.get_ticks_for()
    ticks_list = coinone_api.coinone_tick.api2orm_list(ticks_dict)
    if ticks_list is None:
        logger.info('coinone api return error')
        ticks_list = []

    #ticks_list.insert(0, coinone_api.coinone_tick.default_orm())

    dao.add_all(ticks_list)
    dao.commit()

    after_cnt = dao.query(func.count(CoinoneTick.timestamp)).all()[0][0]
    logger.info('after count: '+str(after_cnt))


if __name__ == '__main__':
    main()


