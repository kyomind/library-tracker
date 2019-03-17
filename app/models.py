# from . import db 這樣也可以，但太抽象不建議
from app import db

# 使用者table
class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True )
    username=db.Column(db.String(64),unique=True ,index=True)
    password=db.Column(db.String(128))
    email=db.Column(db.String(64),unique=True)

    def __repr__(self):
        return f'id={self.id}, username={self.username}, email={self.email}'

