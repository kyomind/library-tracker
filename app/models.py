from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import mylogin

# 使用者資料表
class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True )
    username=db.Column(db.String(64),unique=True ,index=True)
    password=db.Column(db.String(128))
    email=db.Column(db.String(64),unique=True)
    join_time=db.Column(db.DateTime, default=datetime.utcnow)

    books = db.relationship('Book', backref='this_user', lazy='dynamic')

    def __repr__(self):
        return f'user {self.username}'

    def set_password(self,password):
        self.password= generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

# 書籍資料表
class Book(UserMixin, db.Model):
    __tablename__='books'
    id = db.Column(db.Integer,primary_key=True, index=True)
    book_name= db.Column(db.String(128))
    book_id= db.Column(db.String(32))
    copy= db.Column(db.String(32))
    barcode_id= db.Column(db.String(32))
    location= db.Column(db.String(64))
    call_number= db.Column(db.String(32))
    data_type= db.Column(db.String(64))
    status= db.Column(db.String(64))
    reservation= db.Column(db.String(64))
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'[book {self.book_id} {self.book_name}]'





@mylogin.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))