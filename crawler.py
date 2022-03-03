import os
import random
import time
from datetime import datetime, timedelta
from re import findall

import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

from config import mode

MODE_ENV_KEY = os.getenv('FLASK_CONFIG') or 'deploy'
DB_URL = mode[MODE_ENV_KEY].SQLALCHEMY_DATABASE_URI
ENGINE = create_engine(DB_URL)
HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'
}


def get_book_id(book_url):
    """[從使用者輸入的網址取出book_id]

    Args:
        book_url ([str]): [使用者輸入之書籍URL]

    Returns:
        [str]: [取出之book_id]
    """
    book_id_part = findall(r'[?&]id=[1-9]+\d{,5}', book_url)
    book_id = book_id_part[0].split('=')[1]
    return book_id


def get_book_name(book_id):
    """[依book_id取得書名]

    Args:
        book_id ([str]): [book_id]

    Returns:
        [str]: [書名字串]
    """
    url ='http://hylib.ht.org.tw/bookDetail.do?id='
    book_page = requests.get(url+book_id, headers=HEADERS)
    book_page_soup = BeautifulSoup(book_page.text, 'html.parser')
    book_name = book_page_soup.find('h3').text
    return book_name


def get_book_table(book_id):
    """[依book_id取得ajax書籍資料]

    Args:
        book_id ([str]): [book_id]

    Returns:
        [str]: [書籍資料html原始碼字串]
    """
    data = {'id': book_id}
    resp = requests.post(
    'http://hylib.ht.org.tw/maintain/HoldListForBookDetailAjax.do',
    headers=HEADERS, data=data)
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', 'order')
    return table


def get_book_data(book_id):
    """[取得書籍狀態各欄位資料]

    Args:
        book_id ([str]): [book_id]

    Raises:
        ValueError: [無對應書籍資料]

    Returns:
        [list]: [書籍借閱狀態資料]
    """
    book_name = get_book_name(book_id)
    table = get_book_table(book_id)
    if not table:
        raise ValueError('page not exists')
    books = []
    for tr in table.find_all('tr')[1:]:
        book = []
        book.append(book_name)
        book.append(book_id)
        for td in tr.find_all('td'):
            if not td.text:
                continue
            book.append(td.text.strip().strip('/').strip())
            if len(book) > 9:
                book.pop(-2)
        books.append(book)
    return books


def get_update_list_from_db():
    """[取得資料庫所有書籍不重複id，輸出為待更新清單]

    Returns:
        [list]: [待更新狀態書籍id]
    """
    with ENGINE.connect() as conn:
        book_ids = conn.execute('select DISTINCT book_id as id from books')
        book_id_list = [ book['id'] for book in book_ids ]
    return book_id_list


def update_book_data(book_id):
    """[依book_id更新/新增單一本書借閱狀態]

    Args:
        book_id ([str]): [book_id]
    """
    table = get_book_table(book_id)
    books = []
    for tr in table.find_all('tr')[1:]:
        book_dict = {}
        book = []
        book_key = [
            'copy', 'barcode_id', 'location', 'call_number',
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

    if MODE_ENV_KEY in ('heroku', 'deploy'):
        place_holder = '%s'
    else:
        place_holder = '?'
    sql_command = f"""
    UPDATE books SET
        status={place_holder},
        reservation={place_holder},
        update_time={place_holder}
    WHERE book_id={place_holder}
    AND copy={place_holder}"""

    # 將爬蟲結果寫入資料庫，每一本書最多嘗試寫入6次
    interval = 20
    conn = ENGINE.connect()
    for book in books:
        while True:
            try:
                conn.execute(sql_command, book['status'], book['reservation'],
                             datetime.utcnow(), book_id, book['copy'])
            except Exception as err:
                time.sleep(interval)
                interval = interval + 4
                if interval > 40:
                    break
                continue
            else:
                break
    conn.close()


if __name__ == "__main__":
    """[每日單獨執行2次之更新爬蟲]
    """
    book_id_list = get_update_list_from_db()
    print('---')
    print((datetime.utcnow() + timedelta(hours=8)).strftime("%m-%d %H:%M"))
    print('◆開始更新')
    print(book_id_list)
    print(f'共有 {len(book_id_list)} 本書')
    if len(book_id_list) == 0:
        print('資料庫無任何書籍')
    error_count = 0
    for book_id in book_id_list:
        print('開始寫入', book_id)
        try:
            update_book_data(book_id)
        except BaseException as err:
            print(err)
            print('本書更新失敗', f'book_id={book_id}')
            error_count = error_count + 1
            if error_count > 2:
                print('書籍更新失敗達3次，中止更新')
                break
            continue
        print('本書更新完成')
        time.sleep(random.uniform(5, 15))
    print(f'結束更新 {len(book_id_list)} 本書')
    print((datetime.utcnow() + timedelta(hours=8)).strftime("%m-%d %H:%M"))
