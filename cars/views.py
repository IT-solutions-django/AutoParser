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
            ("Корея", ["SAMSUNG", "SSANGYONG", "GENESIS", "HUASONG", "HYUNDAI", "KIA", "기아", "쉐보레(GM대우)", "르노코리아(삼성)", "현대", "제네시스", "KG모빌리티(쌍용)", "대창모터스", "쉐보레(대우)", "기타 수입차", "GM대우", "KG모빌리티", "쌍용", "어울림모터스", "기타 국산차"]),
            ("Япония",
             ["TOYOTA", "NISSAN", "SUZUKI", "MITSUBISHI", "SUBARU", "HONDA", "DAIHATSU", "LEXUS", "ISUZU", "MAZDA",
              "INFINITI", "ACURA", "SCION", "HINO", "도요타", "혼다", "닛산", "토요타", "인피니티", "렉서스", "스즈키", "스바루", "다이하쯔", "미쯔비시", "어큐라", "마쯔다", "다이하쓰", "미쓰비시", "미쯔오카"]),
            ("Китай",
             ["BAIC", "BAO JUN", "BESTURN", "BYD", "CHANGAN", "CHERY", "CIIMO", "DEEPAL", "DENZA", "DONGFENG", "EXEED",
              "FOTON", "GEELY AUTO", "GEOMETRY", "GREAT WALL", "HAMA", "HAVAL", "HIPHI", "HONGQI", "HYCAN", "IM", "JAC",
              "JETOUR", "JETTA", "JMC", "LANTU", "LEAPMOTOR", "LEOPAARD", "LI AUTO", "MAXUS", "NETA AUTO", "NIO", "ORA",
              "QOROS", "RISING AUTO", "REWE", "RUICHI", "SGMW", "SOL", "SOUEAST", "SWM", "TANK", "TRUMPCHI", "VENUCIA",
              "WELTMEISTER", "WEVAN", "WEY", "XPENG MOTORS", "ZEEKR", "ZHONGHUA", "ZOTYE", "ZXAUTO", "LUMMA", "OLEY",
              "KAWEI", "SALEEN", "LINDWIND", "세보모빌리티(캠시스)", "DFSK(동풍자동차)", "북기은상", "동풍소콘"]),
            ("Европа", ["MERCEDES BENZ", "BMW", "MINI", "VOLKSWAGEN", "AUDI", "CITROEN", "VOLVO", "SMART", "PORSCHE",
                        "LAND ROVER", "RENAULT", "ALFAROMEO", "FIAT", "ASTON MARTIN", "JAGUAR", "MG", "PEUGEOT",
                        "MASERATI", "LANCIA", "SAAB", "FERRARI", "ROVER", "BMW ALPINA", "LOTUS", "BENTLEY", "LINCOLN",
                        "TADANO", "TRIUMPH", "BORGWARD", "BRABUS", "BUICK", "CARLSSON", "DS", "HORKI", "KOENIGSEGG",
                        "LAMBORGHINI", "LEVC", "LUXGEN", "LYNK", "MANSORY", "MAYBACH", "MCLAREN", "MORGAN", "POLESTAR",
                        "ROLLS ROYCE", "SEAT", "SKODA", "STARTECH", "IVECO", "ALPINA", "미니", "폭스바겐", "아우디", "푸조", "포르쉐", "볼보", "벤츠", "포드", "쉐보레", "마세라티", "닷지", "랜드로버", "벤틀리", "폴스타", "람보르기니", "스마트", "캐딜락", "시트로엥", "베일리", "링컨", "재규어", "르노(삼성)", "지프", "피아트", "페라리", "크라이슬러", "카라도", "애스턴마틴", "험머", "사브", "롤스로이스", "맥라렌", "시트로엥/DS", "테슬라", "GMC", "DS", "올즈모빌", "로버", "로터스", "르노삼성", "르노코리아", "마이바흐", "부가티", "알핀", "허머", "알파로메오"]),
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
    ip_addr = request.GET.get('ip')
    if not ip_addr or ip_addr != '94.241.142.204':
        return JsonResponse({'error': "Forbidden: Invalid IP from X-Real-IP"}, status=403)

    brand = request.GET.get('brand')
    brand_list = brand.split(',') if brand else []

    drive = request.GET.get('drive')
    drive_list = drive.split(',') if drive else []

    transmission = request.GET.get('transmission')
    transmission_list = transmission.split(',') if transmission else []

    engine_volume_from = request.GET.get('engine_volume_from')
    engine_volume_to = request.GET.get('engine_volume_to')

    model = request.GET.get('model')
    model_list = model.split(',') if model else []

    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')

    car_fuel = request.GET.get('car_fuel')
    car_fuel_list = car_fuel.split(',') if car_fuel else []

    car_type = request.GET.get('car_type')
    car_type_list = car_type.split(',') if car_type else []

    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')

    mileage_from = request.GET.get('mileage_from')
    mileage_to = request.GET.get('mileage_to')

    auction = request.GET.get('auction')

    color = request.GET.get('color')
    color_list = color.split(',') if color else []

    country_str = request.GET.get('country')

    page = int(request.GET.get('page', 1))

    param_filter = Q()

    if brand_list:
        param_filter &= Q(brand__in=brand_list)
    if drive_list:
        param_filter &= Q(drive__in=drive_list)
    if transmission_list:
        param_filter &= Q(transmission__in=transmission_list)
    if model_list:
        param_filter &= Q(model__in=model_list)
    if car_fuel_list:
        param_filter &= Q(engine__in=car_fuel_list)
    if car_type_list:
        param_filter &= Q(body_type__in=car_type_list)
    if auction:
        param_filter &= Q(auction=auction)
    if color_list:
        param_filter &= Q(color__in=color_list)
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
    if country_str:
        param_filter &= Q(brand_country__country=country_str)

    cars = AucCars.objects.filter(param_filter).prefetch_related("photos")

    paginator = Paginator(cars, 16)
    paginated_cars = paginator.get_page(page)

    brands_in_page = {car.brand for car in paginated_cars}

    models_in_page = {car.model for car in paginated_cars}

    brand_translations = {
        t.brand: t.ru_brand
        for t in RuBrandCar.objects.filter(brand__in=brands_in_page)
    }

    model_translations = {
        t.model: t.ru_model
        for t in RuModelCar.objects.filter(model__in=models_in_page)
    }

    cars_list = [
        {
            "id": car.id,
            "brand": car.brand,
            "ru_brand": brand_translations.get(car.brand, car.brand),
            "model": car.model,
            "ru_model": model_translations.get(car.model, car.model),
            "drive": car.drive,
            "transmission": car.transmission,
            "engine_volume": car.engine_volume,
            "year": car.year,
            "price": car.finish,
            "mileage": car.mileage,
            "auction": car.auction,
            "toll": car.toll,
            "photo": list(car.photos.all())[4].url if car.auction == "kcar" and car.photos.count() > 4 else car.photos.first().url if car.photos.exists() else None
        }
        for car in paginated_cars
    ]

    return JsonResponse(
        {"cars": cars_list, "total_pages": paginator.num_pages, "current_page": page},
        json_dumps_params={"ensure_ascii": False},
    )


def get_brands(request):
    ip_addr = request.GET.get('ip')
    if not ip_addr or ip_addr != '94.241.142.204':
        return JsonResponse({'error': "Forbidden: Invalid IP from X-Real-IP"}, status=403)

    country_q = request.GET.get('country')

    brand_country = CountryModels.objects.filter(country=country_q).values_list('brand', flat=True)

    brands_car = RuBrandCar.objects.filter(brand__in=brand_country).values_list('brand', 'ru_brand')

    data_brand = list(brands_car)

    return JsonResponse(data_brand, safe=False, json_dumps_params={"ensure_ascii": False})


def get_models(request):
    ip_addr = request.GET.get('ip')
    if not ip_addr or ip_addr != '94.241.142.204':
        return JsonResponse({'error': "Forbidden: Invalid IP from X-Real-IP"}, status=403)

    brand_car_request = request.GET.get('brand', '').strip()
    brand_list = brand_car_request.split(',') if brand_car_request else []

    if not brand_list:
        return JsonResponse([], safe=False, json_dumps_params={"ensure_ascii": False})

    models_queryset = RuModelCar.objects.filter(
        model__in=AucCars.objects.filter(brand__in=brand_list).values_list('model', flat=True)
    ).values_list('model', 'ru_model')

    return JsonResponse(list(models_queryset), safe=False, json_dumps_params={"ensure_ascii": False})


def get_models_all(request):
    ip_addr = request.GET.get('ip')
    if not ip_addr or ip_addr != '94.241.142.204':
        return JsonResponse({'error': "Forbidden: Invalid IP from X-Real-IP"}, status=403)

    models_queryset = RuModelCar.objects.values_list('model', 'ru_model')

    return JsonResponse(list(models_queryset), safe=False, json_dumps_params={"ensure_ascii": False})


def get_popular_cars(brand):
    cars = AucCars.objects.filter(brand=brand).prefetch_related("photos")[:8]

    brands_in_page = {car.brand for car in cars}

    models_in_page = {car.model for car in cars}

    brand_translations = {
        t.brand: t.ru_brand
        for t in RuBrandCar.objects.filter(brand__in=brands_in_page)
    }

    model_translations = {
        t.model: t.ru_model
        for t in RuModelCar.objects.filter(model__in=models_in_page)
    }

    popular_cars = [
        {
            "id": car.id,
            "brand": car.brand,
            "ru_brand": brand_translations.get(car.brand, car.brand),
            "model": car.model,
            "ru_model": model_translations.get(car.model, car.model),
            "drive": car.drive,
            "transmission": car.transmission,
            "engine_volume": car.engine_volume,
            "year": car.year,
            "price": car.finish,
            "mileage": car.mileage,
            "auction": car.auction,
            "toll": car.toll,
            "photo": list(car.photos.all())[4].url if car.auction == "kcar" and car.photos.count() > 4 else car.photos.first().url if car.photos.exists() else None
        }
        for car in cars
    ]

    return popular_cars


def get_car(request):
    ip_addr = request.GET.get('ip')
    if not ip_addr or ip_addr != '94.241.142.204':
        return JsonResponse({'error': "Forbidden: Invalid IP from X-Real-IP"}, status=403)

    if request.GET.get('id'):
        car_db = AucCars.objects.prefetch_related("photos").select_related("brand_country").get(id=request.GET.get('id'))

        brand_translate = RuBrandCar.objects.filter(brand=car_db.brand).first()

        model_translate = RuModelCar.objects.filter(model=car_db.model).first()

        popular_cars = get_popular_cars(car_db.brand)

        car = {
            "brand": car_db.brand,
            "ru_brand": brand_translate.ru_brand if brand_translate else car_db.brand,
            "model": car_db.model,
            "ru_model": model_translate.ru_model if model_translate else car_db.model,
            "drive": car_db.drive,
            "transmission": car_db.transmission,
            "engine_volume": car_db.engine_volume,
            "year": car_db.year,
            "price": car_db.finish,
            "mileage": car_db.mileage,
            "color": car_db.color,
            "body_type": car_db.body_type,
            "auction": car_db.auction,
            "toll": car_db.toll,
            "engine": car_db.engine,
            "country": car_db.brand_country.country,
            "photos": list(car_db.photos.values_list("url", flat=True))
        }

        return JsonResponse(
            {"car": car, "popular_cars": popular_cars},
            json_dumps_params={"ensure_ascii": False},
        )

    else:
        return JsonResponse(
            {"car": [], "popular_cars": []},
            json_dumps_params={"ensure_ascii": False},
        )


def get_ru_brand(request):
    ip_addr = request.GET.get('ip')
    if not ip_addr or ip_addr != '94.241.142.204':
        return JsonResponse({'error': "Forbidden: Invalid IP from X-Real-IP"}, status=403)

    orig_brand = request.GET.get('brand')
    ru_brand = RuBrandCar.objects.filter(brand=orig_brand).values_list("ru_brand", flat=True).first()

    return JsonResponse(
        {"ru_brand": ru_brand},
        json_dumps_params={"ensure_ascii": False},
    )


def get_ru_model(request):
    ip_addr = request.GET.get('ip')
    if not ip_addr or ip_addr != '94.241.142.204':
        return JsonResponse({'error': "Forbidden: Invalid IP from X-Real-IP"}, status=403)

    orig_model = request.GET.get('model')
    ru_model = RuModelCar.objects.filter(model=orig_model).values_list("ru_model", flat=True).first()

    return JsonResponse(
        {"ru_model": ru_model},
        json_dumps_params={"ensure_ascii": False},
    )
