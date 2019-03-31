import requests
from bs4 import BeautifulSoup
# from app import db
from config import Config
# from app.models import Book
import sqlalchemy as sa

def get_book_id(book_url):
    url=book_url.split('&')[0]
    book_id=url.split('=')[1]
    return book_id

def get_book_data(book_id):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'} 

    url='http://hylib.ht.org.tw/bookDetail.do?id='
    book_page = requests.get(url+book_id, headers=headers)
    book_page_soup = BeautifulSoup(book_page.text, 'html.parser')
    book_name=book_page_soup.find('h3').text

    data = {'id':book_id}
    resp = requests.post(
    'http://hylib.ht.org.tw/maintain/HoldListForBookDetailAjax.do',
    headers=headers, data=data)
    soup = BeautifulSoup(resp.text, 'html.parser')
    table=soup.find('table', 'order')

    books = []
    for tr in table.find_all('tr')[1:]:
        book = []
        book.append(book_name)
        book.append(book_id)
        for td in tr.find_all('td'):
            if td.text == '':
                continue
            book.append(td.text.strip().strip('/').strip())
            if len(book) > 9:
                book.pop(-2)
        books.append(book)
    return books

# 取得資料庫所有書籍不重複id，使用SQLAlchemy但不透過ORM而是用底層SQL語法
def get_update_list_from_db():
    engine = sa.create_engine(Config.SQLALCHEMY_DATABASE_URI)
    conn = engine.connect()
    book_ids=conn.execute('select DISTINCT book_id from books')
    book_id_list= [ book_id[0] for book_id in book_ids ]
    return book_id_list

def update_book_data(lst):
    pass






    