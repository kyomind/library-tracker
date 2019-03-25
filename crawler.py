import requests
from bs4 import BeautifulSoup
import re

def get_book_id(book_url):
    url=book_url.split('&')[0]
    book_id=url.split('=')[1]
    return book_id

def get_book_data(book_id):
    url='http://hylib.ht.org.tw/bookDetail.do?id='
    book_page = requests.get(url+book_id)
    book_page_soup = BeautifulSoup(book_page.text, 'html.parser')
    book_name=book_page_soup.find('h3').text

    data = {'id':book_id}
    resp = requests.post(
    'http://hylib.ht.org.tw/maintain/HoldListForBookDetailAjax.do', data=data)
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









    