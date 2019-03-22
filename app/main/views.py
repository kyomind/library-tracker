from flask import Flask,render_template,redirect,url_for,session,flash
from . import main
from .forms import LoginForm
from app import db
from app.models import User
from flask_login import current_user
from datetime import timedelta

@main.route('/')
def index():
    if session.get('name'):
        return render_template('index.html',name=session.get('name'))
    return render_template('index.html')

@main.route('/user/<name>')
def user(name):
    join_time= current_user.join_time
    time= join_time+timedelta(hours=8)
    return render_template('user.html',name=name,time=time)

@main.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()

    if form.validate_on_submit():
        exist_user=User.query.filter_by(username=
        form.username.data).first()

        if not exist_user:
            new_user=User(username=form.username.data)
            new_user.set_password(form.password.data)

            db.session.add(new_user)
            db.session.commit()

        session['name']=form.username.data
        return redirect(url_for('main.index'))
    return render_template('login.html',form=form)