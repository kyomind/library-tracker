from flask import render_template,redirect,url_for,request,session,flash
from . import auth
from app.auth.forms import LoginForm, RegisterForm, ChangePasswordForm, \
EditEmailForm, RequestResetForm, ResetPasswordForm
from app.models import User
from flask_login import login_user,login_required,logout_user,current_user
from app import db
from app.email import send_email

# 登入
@auth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form=LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(username=
        form.username.data).first()

        if user is not None and user.check_password(form.password.data):
            # 使用login_user()將用戶維持在登入狀態
            login_user(user, remember=form.remember.data)

            flash(u'登入成功！歡迎回來 {}'.format(user.username),'success')
            return redirect(url_for('main.index'))
        flash(u'帳號名稱或密碼錯誤','danger')
    return render_template('auth/login.html',form=form)


# 登出
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# 註冊
@auth.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form=RegisterForm()

    if form.validate_on_submit():
        if form.email.data:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
        else:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(u'註冊成功！請登入','success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

# 變更密碼
@auth.route('/change', methods=['GET','POST'])
@login_required
def change():
    form = ChangePasswordForm()
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

# 新增、修改信箱
@auth.route('/edit', methods=['GET','POST'])
@login_required
def edit():
    form = EditEmailForm()
    user = User.query.filter_by(username=
        current_user.username).first()

    if form.validate_on_submit():
        if not user.check_password(str(form.password.data)):
            flash(u'密碼錯誤','danger')
            return render_template('auth/edit.html',form=form)

        if user.email:
            flash(u'修改信箱成功，請重新驗證','success')
        else:
            flash(u'新增信箱成功，請進行驗證','success')
        
        user.email=form.new_email.data
        user.confirmed=False
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.user',name=current_user.username))

    return render_template('auth/email_edit.html',form=form)

# 重置密碼「請求」頁面
@auth.route('/reset_send', methods=['GET','POST'])
def reset_send():
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            token=user.get_jwt(600)
            url=url_for('auth.reset',_external=True,token=token)
            send_email('重置密碼確認信', user.email, 'mail/reset',
            name=user.username, url=url)
            flash(u'信件已寄出，請至信箱確認','success')
        else:
            pass
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_send.html',form=form)


# 重置密碼(with token)頁面
@auth.route('/reset/<token>', methods=['GET','POST'])
def reset(token):
    if current_user.is_authenticated:
        flash(u'已登入用戶請直接使用「修改密碼」','warning')
        return redirect(url_for('main.index'))
    
    user= User.verify_jwt(token)
    
    if not user:
        flash(u'憑證錯誤或逾期','danger')
        return redirect(url_for('auth.login'))

    form=ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.add(user)
        db.session.commit()
        flash(u'重置密碼成功，請以新密碼登入','success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset.html', form=form, token=token)

# 驗證信箱請求頁面
@auth.route('/confirm')
@login_required
def confirm():
    if current_user.confirmed:
        return redirect(url_for('main.user',name=current_user.username))
    
    if not current_user.email:
        return redirect(url_for('auth.edit'))

    return render_template('auth/confirm.html', email=current_user.email)

# 驗證信箱請求已送出
@auth.route('/confirm_sent')
@login_required
def confirm_sent():
    if current_user.confirmed:
        flash(u'信箱已驗證，請勿重複驗證','warning')
        return redirect(url_for('main.user',name=current_user.username))

    token=current_user.get_jwt(600)
    url=url_for('auth.confirmed',_external=True,token=token)
    send_email('信箱驗證', current_user.email, 'mail/confirm',
    name=current_user.username, url=url)
    return render_template('auth/confirm_sent.html', email=current_user.email)


# 驗證信箱(with token)網址
@auth.route('/confirm/<token>', methods=['GET','POST'])
def confirmed(token):
    if not current_user.is_authenticated:
        flash(u'請登入以進行驗證','danger')
        return redirect(url_for('main.index'))

    user= User.verify_jwt(token)
    if not user:
        flash(u'憑證錯誤或逾期，請重新點選驗證功能','danger')
        return redirect(url_for('main.user',name=user.username))

    user.confirmed=True
    db.session.add(user)
    db.session.commit()
    flash(u'已完成信箱驗證','success')
    return redirect(url_for('main.user',name=user.username))

   
        

