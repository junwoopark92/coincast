# -*- coding: utf-8 -*-
"""
    photolog.photolog_config
    ~~~~~~~~

    photolog 디폴트 설정 모듈.
    photolog 어플리케이션에서 사용할 디폴트 설정값을 담고 있는 클래스를 정의함.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


class CoincastConfig(object):
    #: 데이터베이스 연결 URL
    DB_URL= 'mysql://DEV:coincast@49.142.50.199/CC_DEV?charset=utf8'
    #: 로그 레벨 설정
    LOG_LEVEL = 'info'
    #: 디폴트 로그 파일 경로
    LOG_FILE_PATH = 'resource/log/coincast.log'
    #: 디폴트 SQLAlchemy trace log 설정
    DB_LOG_FLAG = 'True'
    #: 사진 목록 페이징 설정
    PER_PAGE = 10
    


