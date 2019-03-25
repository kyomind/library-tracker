from flask import Flask,render_template,redirect,url_for,session,flash
from . import main
from .forms import LoginForm,AddBookForm
from app import db
from app.models import User,Book
from flask_login import current_user,login_required
from datetime import timedelta
from crawler import get_book_id, get_book_data

@main.route('/')
def index():
    if current_user.is_authenticated:
        books=Book.query.filter_by(this_user=current_user)
        print(books,'分隔線',books[-1].update_time)
        for book in books:
            book.update_time=book.update_time+timedelta(hours=8)
            # book.update_time=book.update_time.strftime("%Y-%m-%d %h:%m")
        return render_template('index.html',books=books)
    return render_template('index.html')

@login_required
@main.route('/user/<name>', methods=['GET','POST'])
def user(name):
    join_time= current_user.join_time
    time= join_time+timedelta(hours=8)
    time= time.strftime("%Y-%m-%d")

    form=AddBookForm()
    book_id=''

    if form.validate_on_submit():
        if form.book_url.data and form.book_id.data:
            if get_book_id(form.book_url.data) != form.book_id.data:
                flash('書目網址與書目id不一致，建議擇一輸入即可')
                return render_template('user.html',name=name,time=time,form=form)
        if form.book_url.data:
            book_id= get_book_id(form.book_url.data)
        if form.book_id.data:
            book_id= form.book_id.data
        print(book_id)
        print(type(book_id))
        if Book.query.filter_by(book_id=book_id).first():
            print(Book.query.filter_by(book_id=book_id).first())
            flash('書籍已存在，無法新增')
            return render_template('user.html',name=name,time=time,form=form)

        books=get_book_data(book_id)
        print(books)


        for book in books:
            data = Book(book_name=book[0], book_id=book[1],
            copy=book[2],barcode_id=book[3],location=book[4],
            call_number=book[5],data_type=book[6],status=book[7],
            reservation=book[8],user_id=current_user.id)
            db.session.add(data)
            db.session.commit()
        flash('書籍新增成功！')
        form=AddBookForm()
        return render_template('user.html',name=name,time=time,form=form)






    return render_template('user.html',name=name,time=time,form=form)
