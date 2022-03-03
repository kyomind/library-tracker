from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL, DataRequired, Optional, Regexp


class AddBookForm(FlaskForm):
    """[新增書目]
    """
    book_url = StringField('請輸入書目網址',
                           validators=[
                               Optional(),
                               URL(message='非正確網址格式'),
                               Regexp(r'.*[?&]id=[1-9]+\d{,5}', message='網址非行天宮圖書館書目網址，或id格式有誤')
                           ])
    book_id = StringField(
        '請輸入書目id',
        validators=[Optional(),
                    Regexp('^[1-9][0-9]{,5}$', message='id格式錯誤，id格式：1到6位正整數')])
    submit = SubmitField('新增書目')


class DeleteBookForm(FlaskForm):
    """[刪除書目]
    """
    book_id = StringField()
    submit = SubmitField()
