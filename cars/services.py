from .models import *
import logging 
import requests
from .sub_fun import calc_toll
import json
from .config import SITE_URLS

logger = logging.getLogger(__name__)


def parse_kcar() -> None: 
    """Заготовка для функции"""
    kcar_setttings = SITE_URLS.KCar
    params = {
        'currentPage': 1, 
        'pageSize': 18, 
        'sIndex': 1, 
        'eIndex': 10, 
        'creatYn': 'N',
    }
    url = kcar_setttings.catalog_url 
    cookies = kcar_setttings.cookies

    response = requests.get(url, params=params, cookies=cookies)
