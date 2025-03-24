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
from datetime import datetime
from bs4 import BeautifulSoup
from django.utils.timezone import now


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


def update_eur_and_usd() -> None: 
    eur = Currency.get_eur() 
    usd = Currency.get_usd() 

    eur_exchange_rate, usd_exchange_rate = get_eur_and_usd_rate() 
    eur.exchange_rate = eur_exchange_rate
    usd.exchange_rate = usd_exchange_rate 

    eur.save()
    usd.save()


def update_all_currencies_from_central_bank() -> None: 
    url = 'https://www.cbr.ru/currency_base/daily/'
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'lxml') 

    currencies = Currency.objects.all()
    for currency in currencies:
        tr_element = soup.find(lambda tag: tag.name == "tr" and tag.find("td", string=currency.name))
        _, curr_code, quantity, _, exchange_rate_raw = map(lambda x: x.text, tr_element.find_all('td'))
        exchange_rate = float(exchange_rate_raw.replace(',', '.')) / int(quantity) 

        currency.exchange_rate_cbr = exchange_rate
        currency.save()


def update_all_currencies_from_tks() -> None: 
    formatted_date = now().strftime("%Y%m%d")
    url = f'https://www.tks.ru/currency/{formatted_date}/' 
    try:
        response = requests.get(url)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        curr_table = soup.find('table', class_='curr_print')
        
        if not curr_table:
            raise ValueError("Таблица с курсами валют не найдена")
            
        for row in curr_table.find_all('tr')[1:]: 
            cols = row.find_all('td')
            if len(cols) < 4:
                continue
                
            curr_name = cols[3].text.strip()
            exchange_rate = float(cols[1].text.strip())
            count = int(cols[2].text.strip())
            
            currency_code = None
            if curr_name == 'ВОН':
                currency_code = 'KRW'
            elif curr_name == 'ЕВРО':
                currency_code = 'EUR'
            elif curr_name == 'ИЕН':
                currency_code = 'JPY'
            elif curr_name == 'ЮАНЬ':
                currency_code = 'CNY'
            elif curr_name == 'ДОЛЛАР США':
                currency_code = 'USD'
                
            if currency_code:
                try:
                    currency = Currency.objects.get(name=currency_code)
                    currency.exchange_rate_tks = exchange_rate / count
                    currency.save()
                except Currency.DoesNotExist:
                    continue
                    
    except requests.RequestException as e:
        print(f"Ошибка при запросе к ТКС: {e}")
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")


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
    today = datetime.today().strftime("%d.%m.%Y")
    params = {
        'date_from': today, 
        'date_to': today
    }
    response = requests.get(krw_url, params)
    try:
        data = response.json()
        krw_exchange_rate = data['DATA'][0]['UF_SALE']
        return float(krw_exchange_rate) / 1000
    except Exception as e:
        print(f'Ошибка при парсинге KRW: {e}') 
        return 1
    

def get_eur_and_usd_rate() -> tuple[float, float]: 
    eur_url = ST.EUR_URL 
    response = requests.get(eur_url)
    data = response.json() 
    try: 
        eur_exchange_rate = data['eur'] 
        usd_exchange_rate = data['usd']
        return eur_exchange_rate, usd_exchange_rate
    except Exception as e:
        print(f'Ошибка при парсинге EUR и ESD: {e}') 
        return 1, 1