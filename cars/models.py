from django.db import models
from django.db.models.signals import m2m_changed, post_delete, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid


class Engine(models.Model):
    class Meta:
        verbose_name = _("Тип топлива")
        verbose_name_plural = _("Типы топлива")

    name = models.CharField(verbose_name=_("Наименование"), max_length=100)

    def __str__(self):
        return f"{self.name}"

class Country(models.Model):
    class Meta:
        verbose_name = _("Страна")
        verbose_name_plural = _("Страны")

    name = models.CharField(verbose_name=_("Страна производителя"), max_length=100)

    def __str__(self):
        return f"{self.name}"
    
class ColorMain(models.Model):
    true_value = models.CharField(verbose_name=_("Цвет"), max_length=100,null=True)
    color = models.CharField(verbose_name=_("Цвет RGBA"), max_length=100,null=True)

    class Meta:
        verbose_name = _("Цвет")
        verbose_name_plural = _("Цвета")


    def __str__(self):
        return f"{self.true_value}"


class Color(models.Model):
    value = models.ForeignKey(ColorMain, verbose_name=_("Цвет"), on_delete=models.CASCADE, related_name='parent_color_api')
    api_value = models.CharField(verbose_name=_('Цвет из апи'),max_length=100,null=True)
    class Meta:
        verbose_name = _("Цвет из апи")
        verbose_name_plural = _("Цвета из апи")


    def __str__(self):
        return f"{self.api_value} ({self.value.true_value})"
    
    @classmethod
    def interpret(cls, api_value):
        try:
            return cls.objects.get(api_value=api_value).true_value
        except cls.DoesNotExist:
            return None
    
    @classmethod
    def reverse_interpret(cls,true_value):
        try:
            return list(cls.objects.filter(true_value=true_value).values_list('api_value', flat = True))
        except cls.DoesNotExist:
            return []


class AucCarsPhoto(models.Model):
    class Meta:
        verbose_name = _("Фото автомобилей с аукционов")
        verbose_name_plural = _("Фото автомобилей с аукционов")
    url = models.CharField(verbose_name=_("URL фотографии"), max_length=500)

    def __str__(self):
        return f"{self.url}"

COUNTRY_CHOICES = (
    ('Япония', "Япония"),
    ('Китай', "Китай"),
    ('Корея', "Корея"),
    ('Европа', "Европа"),
    ('США', "США"),
)


RUBBER_CHOICES = (
    ('Левый руль', "Левый руль"),
    ('Правый руль', "Правый руль"),
)

ENGINE_CHOICES = (
    ('Электро', "Электро"),
    ('Гибрид', "Гибрид"),
    ('Дизель', "Дизель"),
    ('Бензин', "Бензин"),
)

class CountryModels(models.Model):
    class Meta:
        verbose_name = _("Бренды авто по странам производителям")
        verbose_name_plural = _("Бренды авто по странам производителям")

    country = models.CharField(verbose_name=_("Страна производитель"), choices=COUNTRY_CHOICES, max_length=150)
    brand = models.CharField(verbose_name=_("Марка авто"), max_length=150)

    def __str__(self):
        return f"{self.country} {self.brand}"



class AucCarsJapan(models.Model):
    class Meta:
        verbose_name = _("Автомобили Япония")
        verbose_name_plural = _("Автомобили Япония")
        
    auc_table = models.CharField(verbose_name=_("Таблица во внешнем апи"), max_length=50) 
    lot = models.CharField(verbose_name=_("Номер лота"), max_length=50) 
    auc_name = models.CharField(verbose_name=_("Название аукциона"), max_length=50)    
    auc_date = models.DateTimeField(verbose_name=_("Дата аукциона"))    
    api_id = models.CharField(verbose_name=_("ID автомобиля"), max_length=50, unique=True)
    brand_country = models.ForeignKey(CountryModels, verbose_name=_("Страна производитель"), null=True, blank=True, default=None, on_delete=models.CASCADE)
    brand = models.CharField(verbose_name=_("Бренд"), max_length=50)
    model = models.CharField(verbose_name=_("Модель"), max_length=50)
    year = models.IntegerField(verbose_name=_("Год"))
    mileage = models.IntegerField(verbose_name=_("Пробег"))
    photos = models.ManyToManyField(AucCarsPhoto, verbose_name='Фотографии автомобиля')
    price = models.IntegerField(verbose_name=_("Цена в РФ"), null=True, blank=True)
    toll = models.IntegerField(verbose_name=_("Пошлина"), null=True, blank=True)
    kuzov = models.CharField(verbose_name=_("Тип кузова"), max_length=50)
    transmission  = models.CharField(verbose_name=_("Тип КПП"), max_length=50)
    engine_volume = models.CharField(verbose_name=_("Объем двигателя"), max_length=50)
    drive = models.CharField(verbose_name=_("Тип привода"), max_length=50)
    color = models.CharField(verbose_name=_("Цвет"), max_length=50)
    rate = models.CharField(verbose_name=_("Рейтинг"), max_length=5)
    finish = models.CharField(verbose_name=_("Цена в валюте экспортера"), max_length=50)
    power_volume = models.CharField(verbose_name=_("Мощность двигателя"), max_length=30,null=True, blank=True)
    parsing_date = models.DateField(verbose_name=_("Дата парсинга"), auto_now=True)   
    rubber = models.CharField(verbose_name=_("Руль"), max_length=30,null=True, blank=True, choices=RUBBER_CHOICES, default='Левый руль') 
    engine = models.CharField(verbose_name=_("Тип двигателя"), max_length=30,null=True, blank=True, choices=ENGINE_CHOICES, default='Бензин') 
    is_active = models.BooleanField()


    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"
    

class AucCarsChina(models.Model):
    class Meta:
        verbose_name = _("Автомобили Китай")
        verbose_name_plural = _("Автомобили Китай")
        
    auc_table = models.CharField(verbose_name=_("Таблица во внешнем апи"), max_length=50) 
    lot = models.CharField(verbose_name=_("Номер лота"), max_length=50) 
    auc_name = models.CharField(verbose_name=_("Название аукциона"), max_length=50)    
    auc_date = models.DateTimeField(verbose_name=_("Дата аукциона"))    
    api_id = models.CharField(verbose_name=_("ID автомобиля"), max_length=50, unique=True)
    brand_country = models.ForeignKey(CountryModels, verbose_name=_("Страна производитель"), null=True, blank=True,default=None, on_delete=models.CASCADE)
    brand = models.CharField(verbose_name=_("Бренд"), max_length=50)
    model = models.CharField(verbose_name=_("Модель"), max_length=50)
    year = models.IntegerField(verbose_name=_("Год"))
    mileage = models.IntegerField(verbose_name=_("Пробег"))
    photos = models.ManyToManyField(AucCarsPhoto, verbose_name='Фотографии автомобиля')
    price = models.IntegerField(verbose_name=_("Цена в РФ"), null=True, blank=True)
    toll = models.IntegerField(verbose_name=_("Пошлина"), null=True, blank=True)
    kuzov = models.CharField(verbose_name=_("Тип кузова"), max_length=50)
    transmission  = models.CharField(verbose_name=_("Тип КПП"), max_length=50)
    engine_volume = models.CharField(verbose_name=_("Объем двигателя"), max_length=50)
    drive = models.CharField(verbose_name=_("Тип привода"), max_length=50)
    color = models.CharField(verbose_name=_("Цвет"), max_length=50)
    rate = models.CharField(verbose_name=_("Рейтинг"), max_length=5)
    finish = models.CharField(verbose_name=_("Цена в валюте экспортера"), max_length=50)
    power_volume = models.CharField(verbose_name=_("Мощность двигателя"), max_length=30,null=True, blank=True)
    parsing_date = models.DateField(verbose_name=_("Дата парсинга"), auto_now=True)   
    rubber = models.CharField(verbose_name=_("Руль"), max_length=30,null=True, blank=True, choices=RUBBER_CHOICES, default='Левый руль') 
    engine = models.CharField(verbose_name=_("Тип двигателя"), max_length=30,null=True, blank=True, choices=ENGINE_CHOICES, default='Бензин') 
    is_active = models.BooleanField() 


    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"
    
class AucCarsKorea(models.Model):
    class Meta:
        verbose_name = _("Автомобили Корея")
        verbose_name_plural = _("Автомобили Корея")
        
    auc_table = models.CharField(verbose_name=_("Таблица во внешнем апи"), max_length=50) 
    lot = models.CharField(verbose_name=_("Номер лота"), max_length=50) 
    auc_name = models.CharField(verbose_name=_("Название аукциона"), max_length=50)    
    auc_date = models.DateTimeField(verbose_name=_("Дата аукциона"))    
    api_id = models.CharField(verbose_name=_("ID автомобиля"), max_length=50, unique=True)
    brand_country = models.ForeignKey(CountryModels, verbose_name=_("Страна производитель"), null=True, blank=True, default=None, on_delete=models.CASCADE)
    brand = models.CharField(verbose_name=_("Бренд"), max_length=50)
    model = models.CharField(verbose_name=_("Модель"), max_length=50)
    year = models.IntegerField(verbose_name=_("Год"))
    mileage = models.IntegerField(verbose_name=_("Пробег"))
    photos = models.ManyToManyField(AucCarsPhoto, verbose_name='Фотографии автомобиля')
    price = models.IntegerField(verbose_name=_("Цена в РФ"), null=True, blank=True)
    toll = models.IntegerField(verbose_name=_("Пошлина"), null=True, blank=True)
    kuzov = models.CharField(verbose_name=_("Тип кузова"), max_length=50)
    transmission  = models.CharField(verbose_name=_("Тип КПП"), max_length=50)
    engine_volume = models.CharField(verbose_name=_("Объем двигателя"), max_length=50)
    drive = models.CharField(verbose_name=_("Тип привода"), max_length=50)
    color = models.CharField(verbose_name=_("Цвет"), max_length=50)
    rate = models.CharField(verbose_name=_("Рейтинг"), max_length=5)
    finish = models.CharField(verbose_name=_("Цена в валюте экспортера"), max_length=50)
    power_volume = models.CharField(verbose_name=_("Мощность двигателя"), max_length=30,null=True, blank=True)
    parsing_date = models.DateField(verbose_name=_("Дата парсинга"), auto_now=True) 
    rubber = models.CharField(verbose_name=_("Руль"), max_length=30,null=True, blank=True, choices=RUBBER_CHOICES, default='Левый руль') 
    engine = models.CharField(verbose_name=_("Тип двигателя"), max_length=30,null=True, blank=True, choices=ENGINE_CHOICES, default='Бензин') 
    is_active = models.BooleanField()   


    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"
    

# class AucCars(models.Model):
#     class Meta:
#         verbose_name = _("Автомобили")
#         verbose_name_plural = _("Автомобили")
        
#     auc_table = models.CharField(verbose_name=_("Таблица во внешнем апи"), max_length=50) 
#     lot = models.CharField(verbose_name=_("Номер лота"), max_length=50) 
#     auc_name = models.CharField(verbose_name=_("Название аукциона"), max_length=50)    
#     auc_date = models.DateTimeField(verbose_name=_("Дата аукциона"))    
#     api_id = models.CharField(verbose_name=_("ID автомобиля"), max_length=50, unique=True)
#     brand_country = models.ForeignKey(CountryModels, verbose_name=_("Страна производитель"), null=True, blank=True, default=None, on_delete=models.CASCADE)
#     brand = models.CharField(verbose_name=_("Бренд"), max_length=50)
#     model = models.CharField(verbose_name=_("Модель"), max_length=50)
#     year = models.IntegerField(verbose_name=_("Год"))
#     mileage = models.IntegerField(verbose_name=_("Пробег"))
#     photos = models.ManyToManyField(AucCarsPhoto, verbose_name='Фотографии автомобиля')
#     price = models.IntegerField(verbose_name=_("Цена в РФ"), null=True, blank=True)
#     toll = models.IntegerField(verbose_name=_("Пошлина"), null=True, blank=True)
#     kuzov = models.CharField(verbose_name=_("Тип кузова"), max_length=50)
#     transmission  = models.CharField(verbose_name=_("Тип КПП"), max_length=50)
#     engine_volume = models.CharField(verbose_name=_("Объем двигателя"), max_length=50)
#     drive = models.CharField(verbose_name=_("Тип привода"), max_length=50)
#     color = models.CharField(verbose_name=_("Цвет"), max_length=50)
#     rate = models.CharField(verbose_name=_("Рейтинг"), max_length=5)
#     finish = models.CharField(verbose_name=_("Цена в валюте экспортера"), max_length=50)
#     power_volume = models.CharField(verbose_name=_("Мощность двигателя"), max_length=30,null=True, blank=True)
#     parsing_date = models.DateField(verbose_name=_("Дата парсинга"), auto_now=True) 
#     rubber = models.CharField(verbose_name=_("Руль"), max_length=30,null=True, blank=True, choices=RUBBER_CHOICES, default='Левый руль') 
#     engine = models.CharField(verbose_name=_("Тип двигателя"), max_length=30,null=True, blank=True, choices=ENGINE_CHOICES, default='Бензин') 
#     is_active = models.BooleanField()   


#     def __str__(self):
#         return f"{self.brand} {self.model} {self.year}"
    

class AucCarsEurope(models.Model):
    class Meta:
        verbose_name = _("Автомобили Европа")
        verbose_name_plural = _("Автомобили Европа")
        
    auc_table = models.CharField(verbose_name=_("Таблица во внешнем апи"), max_length=50) 
    lot = models.CharField(verbose_name=_("Номер лота"), max_length=50) 
    auc_name = models.CharField(verbose_name=_("Название аукциона"), max_length=50)    
    auc_date = models.DateTimeField(verbose_name=_("Дата аукциона"))    
    api_id = models.CharField(verbose_name=_("ID автомобиля"), max_length=50, unique=True)
    brand_country = models.ForeignKey(CountryModels, verbose_name=_("Страна производитель"), null=True, blank=True, default=None, on_delete=models.CASCADE)
    brand = models.CharField(verbose_name=_("Бренд"), max_length=50)
    model = models.CharField(verbose_name=_("Модель"), max_length=50)
    year = models.IntegerField(verbose_name=_("Год"))
    mileage = models.IntegerField(verbose_name=_("Пробег"))
    photos = models.ManyToManyField(AucCarsPhoto, verbose_name='Фотографии автомобиля')
    price = models.IntegerField(verbose_name=_("Цена в РФ"), null=True, blank=True)
    toll = models.IntegerField(verbose_name=_("Пошлина"), null=True, blank=True)
    kuzov = models.CharField(verbose_name=_("Тип кузова"), max_length=50)
    transmission  = models.CharField(verbose_name=_("Тип КПП"), max_length=50)
    engine_volume = models.CharField(verbose_name=_("Объем двигателя"), max_length=50)
    drive = models.CharField(verbose_name=_("Тип привода"), max_length=50)
    color = models.CharField(verbose_name=_("Цвет"), max_length=50)
    rate = models.CharField(verbose_name=_("Рейтинг"), max_length=5)
    finish = models.CharField(verbose_name=_("Цена в валюте экспортера"), max_length=50)
    power_volume = models.CharField(verbose_name=_("Мощность двигателя"), max_length=30,null=True, blank=True)
    parsing_date = models.DateField(verbose_name=_("Дата парсинга"), auto_now=True)    
    rubber = models.CharField(verbose_name=_("Руль"), max_length=30,null=True, blank=True, choices=RUBBER_CHOICES, default='Левый руль') 
    engine = models.CharField(verbose_name=_("Тип двигателя"), max_length=30,null=True, blank=True, choices=ENGINE_CHOICES, default='Бензин') 
    is_active = models.BooleanField()


    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"
    
class AucCarsRest(models.Model):
    class Meta:
        verbose_name = _("Автомобили (другое)")
        verbose_name_plural = _("Автомобили (другое)")
        
    auc_table = models.CharField(verbose_name=_("Таблица во внешнем апи"), max_length=50) 
    lot = models.CharField(verbose_name=_("Номер лота"), max_length=50) 
    auc_name = models.CharField(verbose_name=_("Название аукциона"), max_length=50)    
    auc_date = models.DateTimeField(verbose_name=_("Дата аукциона"))    
    api_id = models.CharField(verbose_name=_("ID автомобиля"), max_length=50, unique=True)
    brand_country = models.ForeignKey(CountryModels, verbose_name=_("Страна производитель"), null=True, blank=True, default=None, on_delete=models.CASCADE)
    brand = models.CharField(verbose_name=_("Бренд"), max_length=50)
    model = models.CharField(verbose_name=_("Модель"), max_length=50)
    year = models.IntegerField(verbose_name=_("Год"))
    mileage = models.IntegerField(verbose_name=_("Пробег"))
    photos = models.ManyToManyField(AucCarsPhoto, verbose_name='Фотографии автомобиля')
    price = models.IntegerField(verbose_name=_("Цена в РФ"), null=True, blank=True)
    toll = models.IntegerField(verbose_name=_("Пошлина"), null=True, blank=True)
    commission = models.IntegerField(verbose_name=_("Комиссия"), null=True, blank=True)
    kuzov = models.CharField(verbose_name=_("Тип кузова"), max_length=50)
    transmission  = models.CharField(verbose_name=_("Тип КПП"), max_length=50)
    engine_volume = models.CharField(verbose_name=_("Объем двигателя"), max_length=50)
    drive = models.CharField(verbose_name=_("Тип привода"), max_length=50)
    color = models.CharField(verbose_name=_("Цвет"), max_length=50)
    rate = models.CharField(verbose_name=_("Рейтинг"), max_length=5)
    finish = models.CharField(verbose_name=_("Цена в валюте экспортера"), max_length=50)
    power_volume = models.CharField(verbose_name=_("Мощность двигателя"), max_length=30,null=True, blank=True)
    parsing_date = models.DateField(verbose_name=_("Дата парсинга"), auto_now=True)    
    rubber = models.CharField(verbose_name=_("Руль"), max_length=30,null=True, blank=True, choices=RUBBER_CHOICES, default='Левый руль') 
    engine = models.CharField(verbose_name=_("Тип двигателя"), max_length=30,null=True, blank=True, choices=ENGINE_CHOICES, default='Бензин') 
    is_active = models.BooleanField()


    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"