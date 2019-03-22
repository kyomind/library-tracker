from flask import Flask,render_template,redirect,url_for,session,flash
from . import main
from .forms import LoginForm
from app import db
from app.models import User
from flask_login import current_user
from datetime import timedelta

@main.route('/')
def index():
    books=['aa','bb']
    return render_template('index.html',books=books)

@main.route('/user/<name>')
def user(name):
    join_time= current_user.join_time
    time= join_time+timedelta(hours=8)
    time= time.strftime("%Y-%m-%d")
    return render_template('user.html',name=name,time=time)
