import requests
from bs4 import BeautifulSoup

def get_book_id(book_url):
    url=book_url.split('&')[0]

    try:
        book_id=url.split('=')[1]
    except BaseException as err:
        raise('請填入符合圖書館格式之網址')
    return book_id

# def get_book_data(book_id):





    