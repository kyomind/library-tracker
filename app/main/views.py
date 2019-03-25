from flask import Flask,render_template,redirect,url_for,session,flash
from . import main
from .forms import LoginForm,AddBookForm
from app import db
from app.models import User
from flask_login import current_user
from datetime import timedelta
from crawler import get_book_id

@main.route('/')
def index():
    books=[{"barcode": "0275277", "location": "敦化總館/敦化總館", 
    "call_number": "861.57 0251", "status": "已被外借 / 2019-04-08", 
    "reservation": "/ 0人預約", "book_name": "現在,很想見你",
    'data_type':'一般圖書/一般'}]
    return render_template('index.html',books=books)


@main.route('/user/<name>', methods=['GET','POST'])
def user(name):
    join_time= current_user.join_time
    time= join_time+timedelta(hours=8)
    time= time.strftime("%Y-%m-%d")

    form=AddBookForm()

    if form.validate_on_submit():
        if form.book_url.data and form.book_id.data:
            try:
                if get_book_id(form.book_url.data) != form.book_id.data:
                    flash('書目網址與書目id不一致，建議擇一輸入即可')
                    return render_template('user.html',name=name,time=time,form=form)
            except:
                flash('網址格式錯誤，請輸入符合圖書館書目id之網址')
                return render_template('user.html',name=name,time=time,form=form)


        print(form.book_url.data)
        try:
            print(get_book_id(form.book_url.data))
        except :
            flash('網址格式錯誤，請輸入符合圖書館書目id之網址')
        print(form.book_id.data)
        print(type(form.book_id.data))



    return render_template('user.html',name=name,time=time,form=form)
