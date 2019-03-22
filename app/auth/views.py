from flask import render_template,redirect,url_for,request,session,flash
from . import auth
from app.auth.forms import LoginForm, RegisterForm
from app.models import User
from flask_login import login_user,login_required,logout_user
from app import db

# 登入路由
@auth.route('/auth/login', methods=['GET','POST'])
def login():
    form=LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(username=
        form.username.data).first()

        print('tag')

        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            # 暫未加入導向原頁設計

            session['name']=form.username.data
            flash('登入成功！')
            return redirect(url_for('main.index'))
        flash('帳號名稱或密碼錯誤')
    return render_template('auth/login.html',form=form)

# 登出路由
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已經登出了')
    session['name']= ''
    return redirect(url_for('main.index'))

# 註冊路由
@auth.route('/auth/register', methods=['GET','POST'])
def register():
    form=RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('註冊成功！請登入')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)