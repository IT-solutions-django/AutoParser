from django.shortcuts import render
from django.views import View 
from .services import (
    update_jpy, 
    update_cny,
    update_krw,
    update_eur_and_usd,
    update_all_currencies_from_central_bank, 
    update_all_currencies_from_tks,
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
    

class UpdateEurAndUsdView(View): 
    def get(self, request): 
        update_eur_and_usd() 
        return HttpResponse('Курс евро и доллара обновлён')
        

class UpdateFromCentralBank(View): 
    def get(self, request): 
        update_all_currencies_from_central_bank() 
        return HttpResponse('Курсы всех валют обновлены по Центральному банку')
    

class UpdateteFromTks(View): 
    def get(self, request): 
        update_all_currencies_from_tks()
        return HttpResponse('Курсы всех валют обновлены по ТКС')
    

class GetExchangeRatesView(View): 
    def get(self, request): 
        jpy = Currency.get_jpy() 
        cny = Currency.get_cny() 
        krw = Currency.get_krw()
        eur = Currency.get_eur()
        usd = Currency.get_usd()
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
            'EUR': {
                'exchange_rate': eur.exchange_rate, 
                'updated_at': eur.updated_at,
            }, 
            'USD': {
                'exchange_rate': usd.exchange_rate, 
                'updated_at': usd.updated_at,
            }
        }
        return JsonResponse(data)
    

class GetExchangeRatesFromCbrView(View): 
    def get(self, request): 
        jpy = Currency.get_jpy() 
        cny = Currency.get_cny() 
        krw = Currency.get_krw()
        eur = Currency.get_eur()
        usd = Currency.get_usd()
        data = {
            'JPY': {
                'exchange_rate': jpy.exchange_rate_cbr, 
                'updated_at': jpy.updated_at,
            },
            'CNY': {
                'exchange_rate': cny.exchange_rate_cbr, 
                'updated_at': cny.updated_at,
            },
            'KRW': {
                'exchange_rate': krw.exchange_rate_cbr, 
                'updated_at': krw.updated_at,
            },
            'EUR': {
                'exchange_rate': eur.exchange_rate_cbr, 
                'updated_at': eur.updated_at,
            }, 
            'USD': {
                'exchange_rate': usd.exchange_rate_cbr, 
                'updated_at': usd.updated_at,
            }
        }
        return JsonResponse(data)
    

class GetExchangeRatesFromTksView(View): 
    def get(self, request): 
        jpy = Currency.get_jpy() 
        cny = Currency.get_cny() 
        krw = Currency.get_krw()
        eur = Currency.get_eur()
        usd = Currency.get_usd()
        data = {
            'JPY': {
                'exchange_rate': jpy.exchange_rate_tks, 
                'updated_at': jpy.updated_at,
            },
            'CNY': {
                'exchange_rate': cny.exchange_rate_tks, 
                'updated_at': cny.updated_at,
            },
            'KRW': {
                'exchange_rate': krw.exchange_rate_tks, 
                'updated_at': krw.updated_at,
            },
            'EUR': {
                'exchange_rate': eur.exchange_rate_tks, 
                'updated_at': eur.updated_at,
            }, 
            'USD': {
                'exchange_rate': usd.exchange_rate_tks, 
                'updated_at': usd.updated_at,
            }
        }
        return JsonResponse(data)
    

class GetExchangeRatesFromBatareykaView(View): 
    def get(self, request): 
        jpy = Currency.get_jpy() 
        jpy_crypto = Currency.get_jpy_crypto()
        cny = Currency.get_cny() 
        cny_crypto = Currency.get_cny_crypto()
        krw = Currency.get_krw()
        krw_crypto = Currency.get_krw_crypto()
        eur = Currency.get_eur()
        data = {
            'JPY': {
                'exchange_rate': jpy.exchange_rate_batareyka, 
                'updated_at': jpy.updated_at,
            },
            'JPY_crypto': {
                'exchange_rate': jpy_crypto.exchange_rate_batareyka, 
                'updated_at': jpy_crypto.updated_at,
            },
            'CNY': {
                'exchange_rate': cny.exchange_rate_batareyka, 
                'updated_at': cny.updated_at,
            },
            'CNY_crypto': {
                'exchange_rate': cny_crypto.exchange_rate_batareyka, 
                'updated_at': cny_crypto.updated_at,
            },
            'KRW': {
                'exchange_rate': krw.exchange_rate_batareyka, 
                'updated_at': krw.updated_at,
            },
            'KRW_crypto': {
                'exchange_rate': krw_crypto.exchange_rate_batareyka, 
                'updated_at': krw_crypto.updated_at,
            },
            'EUR': {
                'exchange_rate': eur.exchange_rate_batareyka, 
                'updated_at': eur.updated_at,
            }, 
        }
        return JsonResponse(data)
    

# Батарейка


import telebot
import re
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse


bot_token = '8080531459:AAEmBWNCOK7pS8ZcOh6ksncszbaBcGuvn_Y'
bot = telebot.TeleBot(bot_token)


def start_bot():
    bot.remove_webhook()  
    bot.set_webhook(url="https://car-auto.space/bot/")


@csrf_exempt
def webhook(request):
    if request.method == "POST":
        json_str = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)  
        bot.process_new_updates([update]) 
        return HttpResponse("OK", status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)


@bot.message_handler(content_types=['text'])
def callBackOne(message):
    """Получает из Telegram-бота сообщение, парсит его и сохраняет курсы валют"""
    bot.send_message(message.chat.id, text="Обработка сообщения")

    print('Работает')

    if 'йены' in message.text:
            # Регулярное выражение для поиска валют и их курсов
            pattern = r"([^\d\s\W]+[^\d\s]*)(?:\s?=\s?([\d,\.]+)\s?₽(?:\s?\((.*?)\))?)?\s?([\d,\.]+)\s?₽"
            matches = re.findall(pattern,message.text)
            currency_dictionary = {}

            jpy = Currency.get_jpy() 
            jpy_crypto = Currency.get_jpy_crypto()
            cny = Currency.get_cny() 
            cny_crypto = Currency.get_cny_crypto()
            krw = Currency.get_krw()
            krw_crypto = Currency.get_krw_crypto()
            eur = Currency.get_eur()

            for match in matches:
                currency, rate, source, crypto = match
                rate = rate.replace(',', '.')
                crypto = crypto.replace(',', '.')
                if(currency == 'йены'):
                    jpy.exchange_rate_batareyka = float(rate)
                    jpy_crypto.exchange_rate_batareyka = float(crypto)
                    currency_dictionary['JPY'] = float(rate)
                elif(currency == 'воны'):
                    krw.exchange_rate_batareyka = float(rate)
                    krw_crypto.exchange_rate_batareyka = float(crypto)
                    currency_dictionary['KRW'] = float(rate)
                elif(currency == 'юаня'):
                    cny.exchange_rate_batareyka = float(rate)
                    cny_crypto.exchange_rate_batareyka = float(crypto)
                    currency_dictionary['CNY'] = float(rate)
                elif(currency == 'ЦБ'):
                    eur.exchange_rate_batareyka = float(crypto)
                    currency_dictionary['EUR'] = float(crypto)

            for currency in jpy, jpy_crypto, krw, krw_crypto, cny, cny_crypto, eur:
                currency.save()

            bot.send_message(message.chat.id, text="Валюта обновлена")


@bot.message_handler(content_types=['photo'])
def callBackOne(message):
    bot.send_message(message.chat.id, text="Обработка сообщения")
    print(message)
    if message.caption and 'Пост' in message.caption: 
        post_text = message.caption
        for photo in message.photo:
            file_id = photo.file_id
            
            file_info = bot.get_file(file_id)
            file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
            bot.send_message(message.chat.id, text=f"Ссылка на фотографию: {file_url}")
            bot.send_message(message.chat.id, text=f"Текст:\n {post_text}")
        

if __name__ == '__main__':
    start_bot()