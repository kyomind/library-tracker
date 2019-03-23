import requests
from bs4 import BeautifulSoup

url_raw='http://hylib.ht.org.tw/bookDetail.do?id=104838'
url=url_raw.split('&')[0]

try:
    book_id=url.split('=')[1]
except :
    print('請填入符合圖書館格式之網址')




    