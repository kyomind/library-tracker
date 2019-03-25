from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,URL,Regexp,Optional

# 登入表單
class LoginForm(FlaskForm):
    username=StringField('帳號',validators=[DataRequired()])
    password=PasswordField('密碼 ',validators=[DataRequired()])
    remember=BooleanField('記住我')
    submit=SubmitField('登入')

# 新增書目
class AddBookForm(FlaskForm):
    book_url=StringField('請輸入書目網址',validators=[Optional(),
    URL(message='非正確網址格式'),
    Regexp(r'http://hylib.ht.org.tw/bookDetail.do\?id=[1-9]+\d{,5}&?.*$',
        message='網址非行天宮圖書館書目網址，或id格式有誤')])

    book_id=StringField('請輸入書目id',validators=[Optional(),
    Regexp('^[1-9][0-9]{,5}$',flags=0,message=
    'id格式錯誤，id格式：1到6位正整數')])

    submit=SubmitField('新增書目')

