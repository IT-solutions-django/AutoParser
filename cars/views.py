from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import CountryModels
from .tasks import update_korea 
from .auc_parser import parse_korea
from rest_framework import generics
from itertools import chain
from .models import AucCars
from .auc_parser import *




class StartParsingView(View): 
    def get(self, request): 
        update_korea.delay()
        print('Парсер запущен! (только для тестов!)')
        # parse_korea()
        return HttpResponse("Парсер запущен!", status=200)
    

class FetchTestData(View): 
    def get(self, request): 
        sql_query = 'select+*+from+korea+WHERE+1+=+1+limit+1,10'
        user_ip = get_client_ip()
        try:
            url = f"http://78.46.90.228/api/?ip={user_ip}&code=TDAjhTr53Sd9&sql={sql_query}"
            print(url)
            res = requests.get(url)
            soup = BeautifulSoup(res.content.decode("utf-8"), "xml")
            print()
            data = [
                {elem.name: elem.getText() for elem in row.findChildren()}
                for row in soup.findAll("row")
            ]
            print(data)
            return data
        except Exception as e:
            print(f'Ошибка: {e}')

