from django.shortcuts import render
from django.views import View 
from django.http import HttpResponse
from .tasks import parse_korea
from .models import CountryModels
from .tasks import update_korea


class StartParsingView(View): 
    def get(self, request): 
        update_korea.delay() 
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