from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username=StringField('帳號',[DataRequired])
    passowrd=PasswordField('密碼',[DataRequired])
    remember=BooleanField('記住我')
    submit=SubmitField('送出')
