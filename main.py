import requests, bs4
from bs4 import BeautifulSoup
import pandas as pd

# URL страницы для парсинга
main_url = 'https://russian.bwintools.com/'

# Заголовки для запроса (иногда требуется для обхода блокировок)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}

# Отправляем запрос на сайт
def get_soup(url):
    res = requests.get(url, headers)
    return bs4.BeautifulSoup(res.text, 'html.parser')

categories_page = get_soup(main_url+ 'supplier-3949278-cnc-carbide-inserts')
categories = categories_page.findAll('a', class_='image-all')
for cat in categories:
    subcategories_page = get_soup(main_url+cat['href'])
    subcategories_page = categories_page.findAll('a', class_='link')
    for subcat in subcategories_page:
        iphones_page = get_soup(main_url+cat['href'])
        iphones = iphones_page.findAll('div', class_='item-list')
        for iphone in iphones:
            title = iphone.find('a')['title'].strip()
            price = iphone
