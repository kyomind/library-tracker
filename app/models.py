from app import db
from werkzeug.security import generate_password_hash,check_password_hash

# 使用者資料表
class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True )
    username=db.Column(db.String(64),unique=True ,index=True)
    password=db.Column(db.String(128))
    email=db.Column(db.String(64),unique=True)

    def __repr__(self):
        return f'user {self.username}'

    def set_password(self,password):
        self.password= generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)

