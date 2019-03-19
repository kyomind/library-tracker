from flask import Flask,render_template,redirect,url_for,session,flash
from app.forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

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

    if form.validate_on_submit():
        exist_user=User.query.filter_by(username=
        form.username.data).first()
        print(exist_user)

        if not exist_user:
            new_user=User(username=form.username.data,
            password=form.password.data)

            db.session.add(new_user)
            db.session.commit()

        session['name']=form.username.data
        return redirect(url_for('index'))
    return render_template('login.html',form=form)

@app.errorhandler(404)
def not_found(err):
    return render_template('404.html'),404

@app.errorhandler(500)
def server_error(err):
    return render_template('500.html'),500