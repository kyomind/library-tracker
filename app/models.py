from datetime import datetime
import time
from flask import current_app
from flask_login import UserMixin
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import mylogin


# 使用者資料表
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True)
    join_time = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    # 關聯
    books = db.relationship('Book', backref='this_user', lazy='dynamic')

    def __repr__(self):
        return f'user {self.username}'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password,password)

    def get_jwt(self, expire):
        token = jwt.encode(
            {'email': self.email, 'expire': time.time() + expire},
            current_app.config['SECRET_KEY'],
            algorithm='HS256')
        return token

    @classmethod
    def verify_jwt(self, token):
        try:
            answer_dict = jwt.decode(token,current_app.config['SECRET_KEY'],
            algorithm='HS256')
        except:
            return None
        if answer_dict['expire'] < time.time():
            return None
        email = answer_dict['email']
        user = User.query.filter_by(email=email).first()
        return user


# 書籍資料表
class Book(UserMixin, db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, index=True)
    book_name = db.Column(db.String(128))
    book_id = db.Column(db.String(32))
    copy = db.Column(db.String(32))
    barcode_id = db.Column(db.String(32))
    location = db.Column(db.String(64))
    call_number = db.Column(db.String(32))
    data_type = db.Column(db.String(64))
    status = db.Column(db.String(64))
    reservation = db.Column(db.String(64))
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    # 外鍵
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'[book {self.book_id} {self.book_name}]'

    def update(self):
        self.update_time = datetime.utcnow()

@mylogin.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))