from flask import Flask,render_template,redirect,url_for,session,flash
from . import main
from .forms import LoginForm
from app import db
from app.models import User
from flask_login import current_user
from datetime import timedelta

@main.route('/')
def index():
    books=[{"barcode": "0275277", "location": "敦化總館/敦化總館", 
    "call_number": "861.57 0251", "status": "已被外借 / 2019-04-08", 
    "reservation": "/ 0人預約", "book_name": "現在,很想見你",
    'data_type':'一般圖書/一般'}]
    return render_template('index.html',books=books)


@main.route('/user/<name>')
def user(name):
    join_time= current_user.join_time
    time= join_time+timedelta(hours=8)
    time= time.strftime("%Y-%m-%d")
    return render_template('user.html',name=name,time=time)
