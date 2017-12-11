from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, TIMESTAMP
from . import Base

from time import localtime, strftime

def api2orm_list(api_result_dict):
    error_code = api_result_dict['errorCode']
    api_result_dict.pop('errorCode')

    result_state = api_result_dict['result']
    api_result_dict.pop('result')

    if error_code != '0':
        print(error_code)
        return None

    timestamp = int(api_result_dict['timestamp'])
    api_result_dict.pop('timestamp')

    orm_list = []
    for key in api_result_dict.keys():
        temp = api_result_dict[key]
        temp['timestamp'] = timestamp
        orm_list.append(api2orm(temp))

    return orm_list


def api2orm(api_result_dict):
    return CoinoneTick(currency=api_result_dict['currency'],
                       timestamp=api_result_dict['timestamp'],
                       volume=api_result_dict['volume'],
                       yesterday_volume=api_result_dict['yesterday_volume'],
                       first=api_result_dict['first'],
                       last=api_result_dict['last'],
                       high=api_result_dict['high'],
                       low=api_result_dict['low'],
                       yesterday_first=api_result_dict['yesterday_first'],
                       yesterday_last=api_result_dict['yesterday_last'],
                       yesterday_high=api_result_dict['yesterday_high'],
                       yesterday_low=api_result_dict['yesterday_low'])

class CoinoneTick(Base):

    __tablename__ = 'coinone_ticks'

    currency = Column(String(10), primary_key=True)
    timestamp = Column(Integer, primary_key=True)

    volume = Column(Float, unique=False)
    yesterday_volume = Column(Float, unique=False)

    first = Column(Integer, unique=False)
    last = Column(Integer, unique=False)
    high = Column(Integer, unique=False)
    low = Column(Integer, unique=False)

    yesterday_first = Column(Integer, unique=False)
    yesterday_last = Column(Integer, unique=False)
    yesterday_high = Column(Integer, unique=False)
    yesterday_low = Column(Integer, unique=False)

    create_dt = Column(DateTime, unique=False)
    update_dt = Column(DateTime, unique=False)

    def __init__(self, currency, timestamp, volume, yesterday_volume,
                 first, last, high, low, yesterday_first, yesterday_last, yesterday_high, yesterday_low):
        self.currency = currency
        self.timestamp = timestamp
        self.volume = volume
        self.yesterday_volume = yesterday_volume
        self.first = first
        self.last = last
        self.high = high
        self.low = low
        self.yesterday_first = yesterday_first
        self.yesterday_last = yesterday_last
        self.yesterday_high = yesterday_high
        self.yesterday_low = yesterday_low
        self.create_dt = strftime('%Y/%m/%d %H:%M:%S', localtime())
        self.update_dt = self.create_dt






