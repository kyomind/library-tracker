import os
from flask import Flask,render_template,redirect,url_for,session,flash
# from flask_bootstrap import Bootstrap
from .forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# bootstrap=Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///'+ os.path.join(basedir,'tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy()
migrate=Migrate()

from app.models import User

db.init_app(app)
migrate.init_app(app,db)

@app.route('/')
def index():
    if session.get('name'):
        flash('welcome back, this is a FLASH messeage')
        return render_template('index.html',name=session.get('name'))
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    msg=f'帳號={form.username.data},密碼={form.password.data}'
    print(msg)
    

    if form.validate_on_submit():
        session['name']=form.username.data
        return redirect(url_for('index'))
    return render_template('login.html',form=form)

@app.errorhandler(404)
def not_found(err):
    return render_template('404.html'),404

@app.errorhandler(500)
def server_error(err):
    return render_template('500.html'),500