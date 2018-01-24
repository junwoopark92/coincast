import os
import eventlet
from flask import Flask, render_template, request, url_for

socketio = None
thread_manager = None
exchange = None

def print_setting(config):
    print('='*50)
    print('SETTINGH FOR COINCAST APPLICATION')
    print('='*50)
    for key, value in config:
        print('%s=%s' % (key, value))
    print('='*50)


def not_found(error):
    return render_template('404.html'), 404


def server_error(error):
    err_msg = str(error)
    return render_template('500.html', err_msg=err_msg), 500


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)


def create_app(config_file_path='resource/config.cfg'):
    # CONFIG LOAD
    coincast_app = Flask(__name__)
    from coincast.coincast_config import CoincastConfig
    coincast_app.config.from_object(CoincastConfig)
    coincast_app.config.from_pyfile(config_file_path, silent=True)

    from flask_socketio import SocketIO, send
    global socketio
    socketio = SocketIO(coincast_app,async_mode='eventlet')
    print_setting(coincast_app.config.items())

    # LOG INIT
    from coincast.coincast_logger import Log
    log_filepath = os.path.join(coincast_app.root_path,
                                coincast_app.config['LOG_FILE_PATH'])
    Log.init(log_filepath=log_filepath)

    # DB INIT
    from coincast.database import DBManager
    db_url=coincast_app.config['DB_URL']
    DBManager.init(db_url, eval(coincast_app.config['DB_LOG_FLAG']))
    DBManager.init_db()

    # EXCHANGE INIT
    from coincast.api.coinone_exchange import CoinoneExchange
    global exchange
    secretkey = coincast_app.config['SECRETKEY']
    accesstoken = coincast_app.config['ACCESSTOKEN']
    exchange = CoinoneExchange(username='test',secret_key=secretkey,access_token=accesstoken)

    # THREAD INIT
    from coincast.thread import ThreadManager
    global thread_manager
    thread_manager = ThreadManager()

    from coincast.controller import index, real_trader

    from coincast.coincast_blueprint import coincast
    coincast_app.register_blueprint(coincast)

    coincast_app.error_handler_spec[None][404] = not_found
    coincast_app.error_handler_spec[None][500] = server_error

    coincast_app.jinja_env.globals['url_for_other_page'] = \
        url_for_other_page

    return coincast_app, socketio
