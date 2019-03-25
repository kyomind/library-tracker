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
        books=Book.query.filter_by(this_user=current_user).all()
        if len(books) == 0:
            return render_template('index.html',books=books)
        
        # 顯示追縱書籍數量，但同一本書不管有幾本館藏只能算一本
        # 為了達到這個功能，使用了相當迂迴的做法，想不到更簡單的
        item=0
        numbers=[]
        
        # 把所有書的UTC時間改成UTC+8，同時編寫項目數字清單numbers
        for book in books:
            book.update_time=book.update_time+timedelta(hours=8)
            
            # 利用book.copy只有換新一本書才會回到1的特性
            if book.copy=='1':
                item=item+1
            numbers.append(item)

        pair_books=list(zip(numbers,books))

        return render_template('index.html',books=pair_books)
    return render_template('index.html')

@main.route('/user/<name>', methods=['GET','POST'])
@login_required
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

        # 如果資料庫已經「至少有一本」該本書
        if Book.query.filter_by(book_id=book_id).first():
            # 調出該書的全部條目
            same_books=Book.query.filter_by(book_id=book_id).all()
            # 遍歷查詢每一本是否為目前使用者持有
            print(same_books)
            for book in same_books:
                if book.user_id==current_user.id:
                    flash('書籍已存在，無法新增')
                    return render_template('user.html',name=name,time=time,form=form)
            # 好，雖然已經有該本書，但任一本都不是目前使用者持有

            


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
