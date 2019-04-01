from flask import render_template,redirect,url_for,flash
from . import main
from .forms import AddBookForm,DeleteBookForm
from app import db
from app.models import User,Book
from flask_login import current_user,login_required
from datetime import timedelta
from crawler import get_book_id, get_book_data

# 首頁，追縱清單
@main.route('/', methods=['GET','POST'])
def index():

    if current_user.is_authenticated:

        delta=timedelta(hours=8) # 用於模版調整UTC+8
        form=DeleteBookForm()

        books=Book.query.filter_by(this_user=current_user).all()
        if len(books) == 0:
            return render_template('index.html',books=books)
        
        # 顯示追縱書籍數量，但同一本書不管有幾本館藏只能算一本
        # 為了達到這個功能，使用了相當迂迴的做法，想不到更簡單的
        item=0
        numbers=[]
        
        # 創造編號清單
        for book in books:
            # 利用book.copy只有換新一本書才會回到1的特性
            if book.copy=='1':
                item=item+1
            numbers.append(item)        

        numbered_books=tuple(zip(numbers,books))

        # 刪除書目
        if form.validate_on_submit():
            delete_books= Book.query.filter_by(book_id=form.book_id.data,
            user_id= current_user.id).all()
            for book in delete_books:
                db.session.delete(book)
                db.session.commit()
            flash(u'書籍刪除成功','warning')
            return redirect(url_for('main.index'))
        
        return render_template('index.html',books=numbered_books, form=form, delta=delta)

    flash(u'請登入以使用本服務','warning')
    return render_template('index.html')


# 個人頁，新增書目
@main.route('/user/<name>', methods=['GET','POST'])
@login_required
def user(name):
    join_time= current_user.join_time
    time= join_time+timedelta(hours=8)

    form=AddBookForm()

    count=Book.query.filter_by(user_id=current_user.id).group_by(Book.book_id).count()

    if form.validate_on_submit():
        if form.book_url.data and form.book_id.data:
            flash(u'請擇一輸入','danger')
            return redirect(url_for('main.user',name=name))
        elif form.book_url.data:
            book_id= get_book_id(form.book_url.data)
        elif form.book_id.data:
            book_id= form.book_id.data
        else:
            flash(u'請擇一輸入','danger')
            return redirect(url_for('main.user',name=name))

        # 同一本書對「同一使用者」不能重複加入
        # 如果資料庫已經「至少有一本」該本書
        if Book.query.filter_by(book_id=book_id).first():
            # 調出該書的全部條目
            same_books=Book.query.filter_by(book_id=book_id).all()
            
            # 遍歷查詢每一本是否為目前使用者持有
            for book in same_books:
                if book.user_id==current_user.id:
                    flash(u'書籍已存在，無法新增','danger')
                    return redirect(url_for('main.user',name=name))
                last_user_id=book.user_id

            # 為了節省圖書館伺服器資源，要從資料庫複製已有的資料
            copy_books= Book.query.filter_by(book_id=book_id, user_id=last_user_id).all()
            for book in copy_books:
                data = Book(book_name=book.book_name, book_id=book.book_id,
                copy=book.copy,barcode_id=book.barcode_id,location=book.location,
                call_number=book.call_number,data_type=book.data_type,
                status=book.status,reservation=book.reservation,
                user_id=current_user.id, update_time=book.update_time)

                db.session.add(data)
                db.session.commit()
            flash(u'書籍新增成功！','success')
            return redirect(url_for('main.user',name=name))

        try:
            books=get_book_data(book_id)
        except:
            flash(u'很抱歉，無此id之書籍','danger')
            return redirect(url_for('main.user',name=name))

        for book in books:
            data = Book(book_name=book[0], book_id=book[1],
            copy=book[2],barcode_id=book[3],location=book[4],
            call_number=book[5],data_type=book[6],status=book[7],
            reservation=book[8],user_id=current_user.id)

            db.session.add(data)
            db.session.commit()
        flash(u'書籍「{}」新增成功！'.format(book[0]),'success')
        return redirect(url_for('main.user',name=name))

    return render_template('user.html',name=name,time=time,form=form,count=count)
