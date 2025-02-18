import requests 
from bs4 import BeautifulSoup as bs
from .config import SETTINGS as ST
from .models import Currency
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def update_jpy() -> None: 
    jpy = Currency.get_jpy()
    exchange_rate = get_jpy_rate()
    jpy.exchange_rate = exchange_rate
    jpy.save()


def update_cny() -> None: 
    cny = Currency.get_cny() 
    exchange_rate = get_cny_rate()
    cny.exchange_rate = exchange_rate
    cny.save()


def update_krw() -> None: 
    krw = Currency.get_krw() 
    exchange_rate = get_krw_rate() 
    krw.exchange_rate = exchange_rate 
    krw.save()


def get_jpy_rate() -> float:
    jpy_url = ST.JPY_URL
    response = requests.get(jpy_url)
    try:
        soup = bs(response.text, 'lxml')
        jpy_rate = float(soup.find(attrs={'name': 'jpy2'})['value'])
        return jpy_rate

    except Exception as e:
        print(f'Ошибка при парсинге JPY: {e}')
        return 1
    

def get_cny_rate() -> float: 
    cny_url = ST.CNY_URL 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json"
    }
    response = requests.get(cny_url, headers=headers)
    try: 
        data = response.json() 
        cny_rate = next(
            (rate for rate in data["rates"] if rate["currency1"]["code"] == "CNY"),
            None
        )
        if cny_rate:
            exchange_rate = float(cny_rate['offer']) 
            return exchange_rate
    except Exception as e: 
        print(f'Ошибка при парсинге CNY: {e}')
        return 1
    

def get_krw_rate() -> float: 
    krw_url = ST.KRW_URL 
    response = requests.get(krw_url)
    try:
        soup = bs(response.text, 'lxml')
        krw_row = soup.find_all('div', class_='rates__item')[-2] 
        exchange_rate = krw_row.find('p', class_='rates__buy').text
        return float(exchange_rate) / 1000
    except Exception as e:
        print(f'Ошибка при парсинге KRW: {e}')
        return 1