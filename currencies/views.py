from django.shortcuts import render
from django.views import View 
from .services import (
    update_jpy, 
    update_cny,
    update_krw,
)
from django.http import HttpResponse, JsonResponse
from .models import Currency


class UpdateJpyView(View): 
    def get(self, request): 
        update_jpy() 
        return HttpResponse('Курс иены обновлён')
    

class UpdateCnyView(View): 
    def get(self, request): 
        update_cny() 
        return HttpResponse('Курс юаня обновлён')
    

class UpdateKrwView(View): 
    def get(self, request): 
        update_krw() 
        return HttpResponse('Курс воны обновлён')
    

class GetExchangeRatesView(View): 
    def get(self, request): 
        jpy = Currency.get_jpy() 
        cny = Currency.get_cny() 
        krw = Currency.get_krw()
        data = {
            'JPY': {
                'exchange_rate': jpy.exchange_rate, 
                'updated_at': jpy.updated_at,
            },
            'CNY': {
                'exchange_rate': cny.exchange_rate, 
                'updated_at': cny.updated_at,
            },
            'KRW': {
                'exchange_rate': krw.exchange_rate, 
                'updated_at': krw.updated_at,
            },
        }
        return JsonResponse(data)