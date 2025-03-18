from django.db.models import Q
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
from django.core.paginator import Paginator


class StartParsingView(View):
    def get(self, request):
        update_korea.delay()
        # update_korea()
        return HttpResponse("Парсер запущен!", status=200)


class LoadMarksView(View):
    def get(self, request):
        CAR_BRANDS = [
            ("Корея", ["SAMSUNG", "SSANGYONG", "GENESIS", "HUASONG", "HYUNDAI", "KIA"]),
            ("Япония",
             ["TOYOTA", "NISSAN", "SUZUKI", "MITSUBISHI", "SUBARU", "HONDA", "DAIHATSU", "LEXUS", "ISUZU", "MAZDA",
              "INFINITI", "ACURA", "SCION", "HINO"]),
            ("Китай",
             ["BAIC", "BAO JUN", "BESTURN", "BYD", "CHANGAN", "CHERY", "CIIMO", "DEEPAL", "DENZA", "DONGFENG", "EXEED",
              "FOTON", "GEELY AUTO", "GEOMETRY", "GREAT WALL", "HAMA", "HAVAL", "HIPHI", "HONGQI", "HYCAN", "IM", "JAC",
              "JETOUR", "JETTA", "JMC", "LANTU", "LEAPMOTOR", "LEOPAARD", "LI AUTO", "MAXUS", "NETA AUTO", "NIO", "ORA",
              "QOROS", "RISING AUTO", "REWE", "RUICHI", "SGMW", "SOL", "SOUEAST", "SWM", "TANK", "TRUMPCHI", "VENUCIA",
              "WELTMEISTER", "WEVAN", "WEY", "XPENG MOTORS", "ZEEKR", "ZHONGHUA", "ZOTYE", "ZXAUTO", "LUMMA", "OLEY",
              "KAWEI", "SALEEN", "LINDWIND"]),
            ("Европа", ["MERCEDES BENZ", "BMW", "MINI", "VOLKSWAGEN", "AUDI", "CITROEN", "VOLVO", "SMART", "PORSCHE",
                        "LAND ROVER", "RENAULT", "ALFAROMEO", "FIAT", "ASTON MARTIN", "JAGUAR", "MG", "PEUGEOT",
                        "MASERATI", "LANCIA", "SAAB", "FERRARI", "ROVER", "BMW ALPINA", "LOTUS", "BENTLEY", "LINCOLN",
                        "TADANO", "TRIUMPH", "BORGWARD", "BRABUS", "BUICK", "CARLSSON", "DS", "HORKI", "KOENIGSEGG",
                        "LAMBORGHINI", "LEVC", "LUXGEN", "LYNK", "MANSORY", "MAYBACH", "MCLAREN", "MORGAN", "POLESTAR",
                        "ROLLS ROYCE", "SEAT", "SKODA", "STARTECH", "IVECO", "ALPINA"]),
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


def get_filter_cars(request):
    brand = request.GET.get('brand')
    drive = request.GET.get('drive')
    transmission = request.GET.get('transmission')
    engine_volume_from = request.GET.get('engine_volume_from')
    engine_volume_to = request.GET.get('engine_volume_to')
    model = request.GET.get('model')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    car_fuel = request.GET.get('car_fuel')
    car_type = request.GET.get('car_type')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    mileage_from = request.GET.get('mileage_from')
    mileage_to = request.GET.get('mileage_to')
    auction = request.GET.get('auction')
    color = request.GET.getl('color')
    page = int(request.GET.get('page', 1))

    param_filter = Q()

    if brand:
        param_filter &= Q(brand__in=brand)
    if drive:
        param_filter &= Q(drive__in=drive)
    if transmission:
        param_filter &= Q(transmission__in=transmission)
    if model:
        param_filter &= Q(model__in=model)
    if car_fuel:
        param_filter &= Q(engine__in=car_fuel)
    if car_type:
        param_filter &= Q(body_type__in=car_type)
    if auction:
        param_filter &= Q(auction=auction)
    if color:
        param_filter &= Q(color__in=color)
    if engine_volume_from:
        param_filter &= Q(engine_volume__gte=engine_volume_from)
    if engine_volume_to:
        param_filter &= Q(engine_volume__lte=engine_volume_to)
    if year_from:
        param_filter &= Q(year__gte=year_from)
    if year_to:
        param_filter &= Q(year__lte=year_to)
    if price_from:
        param_filter &= Q(finish__gte=price_from)
    if price_to:
        param_filter &= Q(finish__lte=price_to)
    if mileage_from:
        param_filter &= Q(mileage__gte=mileage_from)
    if mileage_to:
        param_filter &= Q(mileage__lte=mileage_to)

    cars = AucCars.objects.filter(param_filter)

    paginator = Paginator(cars, 16)
    paginated_cars = paginator.get_page(page)

    cars_list = [
        {
            "id": car.id,
            "brand": car.brand,
            "model": car.model,
            "drive": car.drive,
            "transmission": car.transmission,
            "engine_volume": car.engine_volume,
            "year": car.year,
            "car_fuel": car.engine,
            "car_type": car.body_type,
            "price": car.finish,
            "mileage": car.mileage,
            "auction": car.auction,
            "color": car.color,
        }
        for car in paginated_cars
    ]

    return JsonResponse(
        {"cars": cars_list, "total_pages": paginator.num_pages, "current_page": page},
        json_dumps_params={"ensure_ascii": False},
    )


def get_brands(request):
    brands_car = RuBrandCar.objects.values_list('brand', 'ru_brand')

    data_brand = list(brands_car)

    return JsonResponse(data_brand, safe=False, json_dumps_params={"ensure_ascii": False})


def get_models(request):
    models_car = RuModelCar.objects.values_list('model', 'ru_model')

    data_model = list(models_car)

    return JsonResponse(data_model, safe=False, json_dumps_params={"ensure_ascii": False})
