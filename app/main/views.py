from flask import Flask,render_template,redirect,url_for,session,flash
from . import main
from .forms import LoginForm
from app import db
from app.models import User

@main.route('/')
def index():
    if session.get('name'):
        flash('welcome back, this is a FLASH messeage')
        return render_template('index.html',name=session.get('name'))
    return render_template('index.html')

@main.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

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

@main.route('/logintest', methods=['GET','POST'])
def login_test():
    form=LoginForm()

    if form.validate_on_submit():
        exist_user=User.query.filter_by(username=
        form.username.data).first()

        print('tag')

        if not exist_user:
            print('wrong username or passowrd')
            return redirect(url_for('main.login_test')) 
        if exist_user.check_password(form.password.data):
            print('登入成功')
            session['name']=form.username.data
            return redirect(url_for('main.index'))
    return render_template('logintest.html',form=form)
