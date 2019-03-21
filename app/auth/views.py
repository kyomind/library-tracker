from flask import render_template,redirect,url_for,request,session,flash
from . import auth
from app.auth.forms import LoginForm 
from app.models import User
from flask_login import login_user,login_required,logout_user


@auth.route('/auth/login', methods=['GET','POST'])
def login():
    form=LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(username=
        form.username.data).first()

        print('tag')

        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember.data)
            # 暫未加入導向原頁設計

            session['name']=form.username.data
            return redirect(url_for('main.index'))
        flash('帳號名稱或密碼錯誤')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已經登出了')
    return redirect(url_for('main.index'))

