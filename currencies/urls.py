from django.urls import path
from .views import *


app_name = 'currencies'


urlpatterns = [
    path('update-jpy/', UpdateJpyView.as_view(), name='update_jpy'),
    path('update-cny/', UpdateCnyView.as_view(), name='update_cny'),
    path('update-krw/', UpdateKrwView.as_view(), name='update_krw'),
    path('update-eur-and-usd/', UpdateEurAndUsdView.as_view(), name='update_eur_and_usd'),

    path('get-exchange-rates/', GetExchangeRatesView.as_view(), name='get_exchange_rates'),
] 