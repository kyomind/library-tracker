import requests
from bs4 import BeautifulSoup
from config import Config
import sqlalchemy as sa
import time
import random
from datetime import datetime

def get_book_id(book_url):
    url=book_url.split('&')[0]
    book_id=url.split('=')[1]
    return book_id

def get_book_name(book_id):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'} 

    url='http://hylib.ht.org.tw/bookDetail.do?id='
    book_page = requests.get(url+book_id, headers=headers)
    book_page_soup = BeautifulSoup(book_page.text, 'html.parser')
    book_name=book_page_soup.find('h3').text
    return book_name

def get_book_table(book_id):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'} 
    
    data = {'id': book_id}
    resp = requests.post(
    'http://hylib.ht.org.tw/maintain/HoldListForBookDetailAjax.do',
    headers=headers, data=data)
    soup = BeautifulSoup(resp.text, 'html.parser')
    table=soup.find('table', 'order')
    return table

def get_book_data(book_id):
    book_name=get_book_name(book_id)
    table=get_book_table(book_id)

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

# 取得資料庫所有書籍不重複id
def get_update_list_from_db():
    engine = sa.create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.begin() as conn:
        book_ids=conn.execute('select DISTINCT book_id from books')
        book_id_list= [ book_id[0] for book_id in book_ids ]
    return book_id_list

def update_book_data(book_id):
    table=get_book_table(book_id)
    
    books = []
    for tr in table.find_all('tr')[1:]:
        book_dict = {}
        book = []
        book_key = [
            'copy', 'barcode_id', 'location','call_number',
            'data_type', 'status', 'reservation'
        ]
        for td in tr.find_all('td'):
            if td.text == '':
                continue
            book.append(td.text.strip().strip('/').strip())
            if len(book) > 7:
                book.pop(-2)
            book_dict = dict(zip(book_key, book))
        books.append(book_dict)
    
    engine = sa.create_engine(Config.SQLALCHEMY_DATABASE_URI)
    conn = engine.connect()
    sql_command='UPDATE books SET status=?, reservation=?, \
    update_time=? WHERE book_id=? AND copy=?'

    interval=20
    for book in books:
        while True:
            try:
                conn.execute(sql_command, book['status'], 
                book['reservation'], datetime.utcnow(), 
                book_id,book['copy'])
            except BaseException as err:
                print(err)
                time.sleep(interval)
                interval=interval+4
                if interval > 40:
                    break
                continue
            else:
                break
    conn.close()
    

if __name__ == "__main__":
    book_id_list=get_update_list_from_db()
    print(book_id_list,f'共有{len(book_id_list)}本書')
    error_count=0
    for book_id in book_id_list:
        print('開始寫入',book_id)
        try:
            update_book_data(book_id)
        except BaseException as err:
            print(err)
            print('本書更新失敗',f'book_id={book_id}')
            error_count= error_count+1
            if error_count > 2:
                print('書籍更新失敗達3次，中止更新')
                break
            continue
        print('本書完成')
        time.sleep(random.uniform(3.14159, 16.18033))



    