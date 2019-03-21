from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp,ValidationError
from app.models import User

# 登入表單
class LoginForm(FlaskForm):
    username=StringField('帳號',validators=[DataRequired()])
    password=PasswordField('密碼 ',validators=[DataRequired()])
    remember=BooleanField('記住我')
    submit=SubmitField('登入')

# 註冊表單
class RegisterForm(FlaskForm):
    username= StringField('帳號',validators=[DataRequired(),
    Regexp('^[A-Za-z][A-Za-z0-9]*$',flags=0,message=
    '帳號格式：大寫或小寫英文字母開頭，可包括數字，不含特殊符號'),
    Length(3,15,message='帳號長度為3至15字元')])
    password= PasswordField('密碼 ',validators=[DataRequired(),
    EqualTo('password2',message='輸入的密碼不一致')])
    password2= PasswordField('再次確認密碼 ',validators=[DataRequired()])
    email= StringField('信箱',validators=[DataRequired(),
    Email(message='信箱格式有誤')])
    submit= SubmitField('註冊')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('帳號已存在')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('信箱已被註冊')