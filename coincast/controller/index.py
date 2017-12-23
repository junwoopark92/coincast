# -*- coding: utf-8 -*-
from coincast.coincast_blueprint import coincast
from flask import redirect, url_for, render_template


@coincast.route('/')
def index():
    """로그인이 성공한 다음에 보여줄 초기 페이지"""
    return render_template('index.html')


@coincast.route('/temp')
def temp():
    return render_template('temp.html')