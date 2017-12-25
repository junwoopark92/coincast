# -*- coding: utf-8 -*-
from coincast.coincast_blueprint import coincast
from coincast import socketio
from flask import redirect, url_for, render_template
from flask_socketio import send
from coincast.database import dao
from coincast.model.coinone_tick import CoinoneTick
from coincast import thread_manager


@coincast.route('/')
def index():
    """로그인이 성공한 다음에 보여줄 초기 페이지"""
    return render_template('index.html')


@coincast.route('/temp')
def temp():
    #thread_manager.run(func, 'show_tick', True, 3, [])
    return render_template('temp.html')


# @socketio.on('message', namespace='/tick')
# def handleMessage(msg):
#     print('Message: ' + msg)
#     send(msg, broadcast=True)




