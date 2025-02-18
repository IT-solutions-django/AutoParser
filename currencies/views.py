from django.shortcuts import render
from django.views import View 
from .services import (
    update_jpy, 
    update_cny,
    update_krw,
)
from django.http import HttpResponse


class UpdateJpyView(View): 
    def get(self, request): 
        update_jpy() 
        return HttpResponse('Кайф')
    

class UpdateCnyView(View): 
    def get(self, request): 
        update_cny() 
        return HttpResponse('Кайф')
    

class UpdateKrwView(View): 
    def get(self, request): 
        update_krw() 
        return HttpResponse('Кайф')