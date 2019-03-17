from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired

# 註冊表單
class LoginForm(FlaskForm):
    username=StringField('帳號  ',validators=[DataRequired()])
    password=PasswordField('密碼 ',validators=[DataRequired()])
    remember=BooleanField('記住我')
    submit=SubmitField('送出')
