from flask import Flask,render_template,redirect,url_for,session,flash
from . import main
from .forms import LoginForm,AddForm,DeleteForm
from app import db
from app.models import User,Book
from flask_login import current_user,login_required
from datetime import timedelta
from crawler import get_book_id, get_book_data

@main.route('/', methods=['GET','POST'])
def index():

    if current_user.is_authenticated:

        form=DeleteForm()
        if form.validate_on_submit():
            print(form.book_id.data,'ahah')



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

        pair_books=tuple(zip(numbers,books))

        return render_template('index.html',books=pair_books, form=form)

    return render_template('index.html')





@main.route('/user/<name>', methods=['GET','POST'])
@login_required
def user(name):
    join_time= current_user.join_time
    time= join_time+timedelta(hours=8)
    time= time.strftime("%Y-%m-%d")

    form=AddForm()
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

        # 同一本書對「同一使用者」不能重複加入
        # 如果資料庫已經「至少有一本」該本書
        if Book.query.filter_by(book_id=book_id).first():
            # 調出該書的全部條目
            same_books=Book.query.filter_by(book_id=book_id).all()
            
            # 遍歷查詢每一本是否為目前使用者持有
            for book in same_books:
                if book.user_id==current_user.id:
                    flash('書籍已存在，無法新增')
                    return render_template('user.html',name=name,time=time,form=form)
                last_user_id=book.user_id
            # 好，雖然資料庫已存在該本書，但都不是目前使用者持有
            # 確定使用者可以新增該書

            # 雖然流程可以繼續，直接再爬蟲一次就好了
            # 但為了節省圖書館的資源與自我挑戰，要從資料庫複製已有的資料
            # 難點在於，單本圖書，館藏數在二以上，怎麼把每一筆資料都複製
            # 其次，如果擁有該書的用戶數也在二以上，只能複製單一用戶的資料！

            copy_books= Book.query.filter_by(book_id=book_id, user_id=last_user_id).all()
            for book in copy_books:
                data = Book(book_name=book.book_name, book_id=book.book_id,
                copy=book.copy,barcode_id=book.barcode_id,location=book.location,
                call_number=book.call_number,data_type=book.data_type,
                status=book.status,reservation=book.reservation,
                user_id=current_user.id, update_time=book.update_time)

                db.session.add(data)
                db.session.commit()
            flash('書籍新增成功！')
            return redirect(url_for('main.user',name=name,time=time,form=form))



        books=get_book_data(book_id)


        for book in books:
            data = Book(book_name=book[0], book_id=book[1],
            copy=book[2],barcode_id=book[3],location=book[4],
            call_number=book[5],data_type=book[6],status=book[7],
            reservation=book[8],user_id=current_user.id)

            db.session.add(data)
            db.session.commit()
        flash('書籍新增成功！')
        return redirect(url_for('main.user',name=name,time=time,form=form))

    return render_template('user.html',name=name,time=time,form=form)
