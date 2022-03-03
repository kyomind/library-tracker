from datetime import timedelta

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.main import main
from app.main.forms import AddBookForm, DeleteBookForm
from app.models import Book, User
from crawler import ENGINE, MODE_ENV_KEY, get_book_data, get_book_id


@main.route('/', methods=['GET', 'POST'])
def index():
    """[未登入用戶首頁/已登入用戶追縱清單]
    """
    if current_user.is_authenticated:
        delta = timedelta(hours=8)  # 用於模版調整時間為UTC+8
        form = DeleteBookForm()

        # 目前使用者的所有藏書
        books = Book.query.filter_by(this_user=current_user).all()
        if len(books) == 0:
            return render_template('index.html', books=books)

        # 顯示追縱書籍數量編號，同一本書不管有幾本館藏，編號上只能算一本
        number = 0
        numbers = []
        for book in books:
            if book.copy == '1':
                number = number + 1
            numbers.append(number)
        numbered_books = tuple(zip(numbers, books))
        # 刪除書目(一本書可能有複數本館藏，在清單上有複數列)
        if form.validate_on_submit():
            delete_books = Book.query.filter_by(book_id=form.book_id.data,
                                                user_id=current_user.id).all()
            for book in delete_books:
                db.session.delete(book)
                db.session.commit()
            flash(u'書籍刪除成功', 'warning')
            return redirect(url_for('main.index'))
        return render_template('index.html', books=numbered_books, form=form, delta=delta)
    flash(u'請登入以使用本服務', 'warning')
    return render_template('index.html')


@main.route('/user/<name>', methods=['GET', 'POST'])
@login_required
def user(name):
    """[個人頁/新增書目]

    Args:
        name ([str]): [用戶名]
    """
    join_time = current_user.join_time
    time = join_time + timedelta(hours=8)
    form = AddBookForm()

    # 新增書目
    if form.validate_on_submit():
        # 輸入欄位值檢查
        if form.book_url.data and form.book_id.data:
            flash(u'請擇一輸入', 'danger')
            return redirect(url_for('main.user', name=name))
        elif form.book_url.data:
            book_id = get_book_id(form.book_url.data)
        elif form.book_id.data:
            book_id = form.book_id.data
        else:
            flash(u'請擇一輸入', 'danger')
            return redirect(url_for('main.user', name=name))
        # 同一本書對「同一使用者」不能重複加入
        # 如果資料庫已經「至少有一本」該本書
        if Book.query.filter_by(book_id=book_id).first():
            # 調出該書的全部條目
            same_books = Book.query.filter_by(book_id=book_id).all()
            # 遍歷查詢每一本是否為目前使用者持有
            for book in same_books:
                if book.user_id == current_user.id:
                    flash(u'新增失敗：你已收藏本書', 'danger')
                    return redirect(url_for('main.user', name=name))
                # 記錄最後一列的持有者id，將複製此份圖書資料
                last_user_id = book.user_id
            # 從資料庫複製已有的圖書資料
            copy_books = Book.query.filter_by(book_id=book_id, user_id=last_user_id).all()
            for book in copy_books:
                data = Book(book_name=book.book_name,
                            book_id=book.book_id,
                            copy=book.copy,
                            barcode_id=book.barcode_id,
                            location=book.location,
                            call_number=book.call_number,
                            data_type=book.data_type,
                            status=book.status,
                            reservation=book.reservation,
                            user_id=current_user.id,
                            update_time=book.update_time)
                db.session.add(data)
                db.session.commit()
            flash(u'新增成功！書名：{}'.format(book.book_name), 'success')
            return redirect(url_for('main.user', name=name))

        # 資料庫不存在該book_id之書籍，必須重新爬蟲、新增
        try:
            books = get_book_data(book_id)
        except:
            flash(u'新增失敗：查無此id之書籍', 'danger')
            return redirect(url_for('main.user', name=name))
        for book in books:
            data = Book(book_name=book[0],
                        book_id=book[1],
                        copy=book[2],
                        barcode_id=book[3],
                        location=book[4],
                        call_number=book[5],
                        data_type=book[6],
                        status=book[7],
                        reservation=book[8],
                        user_id=current_user.id)
            db.session.add(data)
            db.session.commit()
        flash(u'新增成功！書名：{}'.format(book[0]), 'success')
        return redirect(url_for('main.user', name=name))
    return render_template('user.html', name=name, time=time, form=form)
