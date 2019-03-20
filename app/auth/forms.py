from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired

# 登入表單
class LoginForm(FlaskForm):
    username=StringField('帳號  ',validators=[DataRequired()])
    password=PasswordField('密碼 ',validators=[DataRequired()])
    remember=BooleanField('記住我')
    submit=SubmitField('auth登入')
