from django.urls import path
from .views import *


app_name = 'currencies'


urlpatterns = [
    path('update-jpy/', UpdateJpyView.as_view(), name='update_jpy'),
    path('update-cny/', UpdateCnyView.as_view(), name='update_cny'),
    path('update-krw/', UpdateKrwView.as_view(), name='update_krw'),
    path('update-eur-and-usd/', UpdateEurAndUsdView.as_view(), name='update_eur_and_usd'),

    path('update-currencies-from-cbr/', UpdateFromCentralBank.as_view(), name='update_from_central_bank'),
    path('update-currencies-from-tks/', UpdateteFromTks.as_view(), name='update_from_tks'),

    path('get-exchange-rates/', GetExchangeRatesView.as_view(), name='get_exchange_rates'),
    path('get-exchange-rates-from-cbr/', GetExchangeRatesFromCbrView.as_view(), name='get_exchange_rates_from_cbr'),
    path('get-exchange-rates-from-tks/', GetExchangeRatesFromBatareykaView.as_view(), name='get_exchange_rates_from_tks'),
    path('get-exchange-rates-from-batareyka/', GetExchangeRatesFromBatareykaView.as_view(), name='get_exchange_rates_from_batareyka'),
] 