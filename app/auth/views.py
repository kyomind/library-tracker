from flask import render_template,redirect,url_for,request,session,flash
from . import auth
from app.auth.forms import LoginForm, RegisterForm, ChangePasswordForm, \
EditEmailForm, RequestResetForm, ResetPasswordForm
from app.models import User
from flask_login import login_user,login_required,logout_user,current_user
from app import db
from app.email import send_email

# 登入
@auth.route('/auth/login', methods=['GET','POST'])
def login():
    form=LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(username=
        form.username.data).first()

        if user is not None and user.check_password(form.password.data):
            # 使用login_user()將用戶維持在登入狀態
            login_user(user, remember=form.remember.data)

            flash(u'登入成功！','success')
            return redirect(url_for('main.index'))
        flash(u'帳號名稱或密碼錯誤','danger')
    return render_template('auth/login.html',form=form)

# 登出
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'你已經登出了','warning')
    session['name']= ''
    return redirect(url_for('main.index'))

# 註冊
@auth.route('/auth/register', methods=['GET','POST'])
def register():
    form=RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(u'註冊成功！請登入','success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

# 變更密碼
@auth.route('/auth/change', methods=['GET','POST'])
@login_required
def change():
    form= ChangePasswordForm()
    user = User.query.filter_by(username=
        current_user.username).first()

    if form.validate_on_submit():
        if not user.check_password(str(form.old_password.data)):
            flash(u'舊密碼錯誤','danger')
            return render_template('auth/change.html',form=form)

        user.set_password(form.new_password.data)
        db.session.add(user)
        db.session.commit()
        flash(u'變更密碼成功','success')
        return redirect(url_for('main.user',name=current_user.username))
    return render_template('auth/change.html',form=form)

# 修改信箱
@auth.route('/auth/edit', methods=['GET','POST'])
@login_required
def edit():
    form= EditEmailForm()
    user = User.query.filter_by(username=
        current_user.username).first()

    if form.validate_on_submit():
        if not user.check_password(str(form.password.data)):
            flash(u'密碼錯誤','danger')
            return render_template('auth/edit.html',form=form)

        user.email=form.new_email.data
        db.session.add(user)
        db.session.commit()
        flash(u'修改信箱成功','success')
        return redirect(url_for('main.user',name=current_user.username))

    return render_template('auth/edit.html',form=form)

# 重置密碼「請求」頁面
@auth.route('/auth/reset', methods=['GET','POST'])
def reset():
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            token=user.get_jwt(600)
            url=url_for('auth.token',_external=True,token=token)
            send_email('重置密碼確認信', user.email, url,
            f"<h1>{url}<h1>")
            flash(u'信件已寄出，請至信箱確認','success')
        else:
            pass
        return redirect(url_for('auth.login'))

    return render_template('auth/reset.html',form=form)

# 重置密碼token頁面
@auth.route('/auth/<token>', methods=['GET','POST'])
def token(token):
    form=ResetPasswordForm()
    return render_template('auth/token.html', form=form, token=token)



   
        

