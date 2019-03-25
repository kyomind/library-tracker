import requests
from bs4 import BeautifulSoup
import re

def get_book_id(book_url):
    url=book_url.split('&')[0]
    book_id=url.split('=')[1]
    return book_id

# def get_book_data(book_id):





    