# -*- coding: utf-8 -*-

from flask import Blueprint
from coincast.coincast_logger import Log

coincast = Blueprint('coincast', __name__,
                     template_folder='templates', static_folder='static')

Log.info('static folder : %s' % coincast.static_folder)
Log.info('template folder : %s' % coincast.template_folder)
