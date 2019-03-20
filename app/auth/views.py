from flask import render_template,redirect,url_for,request,session
from . import auth
from app.auth.forms import LoginForm 
from app.models import User
from flask_login import login_user




@auth.route('/auth/login', methods=['GET','POST'])
def login():
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
    return render_template('auth/login.html',form=form)
