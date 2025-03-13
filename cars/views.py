from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import CountryModels
from .tasks import update_korea 
from .auc_parser import parse_korea
from rest_framework import generics
from itertools import chain
from .models import AucCars
from .auc_parser import *
from .services import parse_kcar, translate_and_save




class StartParsingView(View): 
    def get(self, request): 
        update_korea.delay()
        # update_korea()
        return HttpResponse("Парсер запущен!", status=200)


class LoadMarksView(View): 
    def get(self, request): 
        CAR_BRANDS = [
            ("Корея", ["SAMSUNG", "SSANGYONG", "GENESIS", "HUASONG", "HYUNDAI", "KIA"]),
            ("Япония", ["TOYOTA", "NISSAN", "SUZUKI", "MITSUBISHI", "SUBARU", "HONDA", "DAIHATSU", "LEXUS", "ISUZU", "MAZDA", "INFINITI", "ACURA", "SCION", "HINO"]),
            ("Китай", ["BAIC", "BAO JUN", "BESTURN", "BYD", "CHANGAN", "CHERY", "CIIMO", "DEEPAL", "DENZA", "DONGFENG", "EXEED", "FOTON", "GEELY AUTO", "GEOMETRY", "GREAT WALL", "HAMA", "HAVAL", "HIPHI", "HONGQI", "HYCAN", "IM", "JAC", "JETOUR", "JETTA", "JMC", "LANTU", "LEAPMOTOR", "LEOPAARD", "LI AUTO", "MAXUS", "NETA AUTO", "NIO", "ORA", "QOROS", "RISING AUTO", "REWE", "RUICHI", "SGMW", "SOL", "SOUEAST", "SWM", "TANK", "TRUMPCHI", "VENUCIA", "WELTMEISTER", "WEVAN", "WEY", "XPENG MOTORS", "ZEEKR", "ZHONGHUA", "ZOTYE", "ZXAUTO", "LUMMA", "OLEY", "KAWEI", "SALEEN", "LINDWIND"]),
            ("Европа", ["MERCEDES BENZ", "BMW", "MINI", "VOLKSWAGEN", "AUDI", "CITROEN", "VOLVO", "SMART", "PORSCHE", "LAND ROVER", "RENAULT", "ALFAROMEO", "FIAT", "ASTON MARTIN", "JAGUAR", "MG", "PEUGEOT", "MASERATI", "LANCIA", "SAAB", "FERRARI", "ROVER", "BMW ALPINA", "LOTUS", "BENTLEY", "LINCOLN", "TADANO", "TRIUMPH", "BORGWARD", "BRABUS", "BUICK", "CARLSSON", "DS", "HORKI", "KOENIGSEGG", "LAMBORGHINI", "LEVC", "LUXGEN", "LYNK", "MANSORY", "MAYBACH", "MCLAREN", "MORGAN", "POLESTAR", "ROLLS ROYCE", "SEAT", "SKODA", "STARTECH", "IVECO", "ALPINA"]),
        ]
        for country, brands in CAR_BRANDS:
            for brand in brands:
                CountryModels.objects.get_or_create(country=country, brand=brand)


class DeleteMarksView(View): 
    def get(self, request): 
        CountryModels.objects.all().delete()


class ParseKcarView(View): 
    def get(self, request): 
        parse_kcar() 
        return HttpResponse('Парсинг kcar.com')


class TranslateMark(View):
    def get(self, request):
        translate_and_save("RuBrandCar", "brand", "ru_brand")
        return HttpResponse('Перевод марок авто')


class TranslateModel(View):
    def get(self, request):
        translate_and_save("RuModelCar", "model", "ru_model")
        return HttpResponse('Перевод моделей авто')


class TranslateColor(View):
    def get(self, request):
        translate_and_save("RuColorCar", "color", "ru_color", target_language='ru')
        return HttpResponse('Перевод цветов авто')
