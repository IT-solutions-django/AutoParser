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


class AucCars(models.Model):
    class Meta:
        verbose_name = _("Автомобили")
        verbose_name_plural = _("Автомобили")

    lot = models.CharField(verbose_name=_("Номер лота"), max_length=50)
    api_id = models.CharField(verbose_name=_("ID автомобиля"), max_length=50, unique=True)
    brand_country = models.ForeignKey(CountryModels, verbose_name=_("Страна производитель"), null=True, blank=True, default=None, on_delete=models.CASCADE)
    brand = models.CharField(verbose_name=_("Бренд"), max_length=50)
    model = models.CharField(verbose_name=_("Модель"), max_length=50)
    year = models.IntegerField(verbose_name=_("Год"))
    mileage = models.IntegerField(verbose_name=_("Пробег"))
    photos = models.ManyToManyField(AucCarsPhoto, verbose_name='Фотографии автомобиля')
    toll = models.IntegerField(verbose_name=_("Пошлина"), null=True, blank=True)
    body_type = models.CharField(verbose_name=_("Тип кузова"), max_length=50, null=True, blank=True)
    body_brand = models.CharField(verbose_name=_("Кузов"), null=True, blank=True, max_length=50)
    transmission  = models.CharField(verbose_name=_("Тип КПП"), max_length=50)
    engine_volume = models.CharField(verbose_name=_("Объем двигателя"), max_length=50)
    drive = models.CharField(verbose_name=_("Тип привода"), max_length=50)
    color = models.CharField(verbose_name=_("Цвет"), max_length=50)
    rate = models.CharField(verbose_name=_("Рейтинг"), max_length=50)
    finish = models.CharField(verbose_name=_("Цена в валюте экспортера"), max_length=50)
    power_volume = models.CharField(verbose_name=_("Мощность двигателя"), max_length=30,null=True, blank=True)
    parsing_date = models.DateField(verbose_name=_("Дата парсинга"), auto_now=True)
    engine = models.CharField(verbose_name=_("Тип двигателя"), max_length=30,null=True, blank=True, choices=ENGINE_CHOICES, default='Бензин')
    is_active = models.BooleanField()
    month = models.CharField('Месяц', max_length=20, null=True, blank=True)
    grade = models.CharField('Комплектация', max_length=200, null=True, blank=True)
    equip = models.CharField('Детали комплектации', max_length=200, null=True, blank=True)
    auction = models.CharField('Аукцион', max_length=50)


    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"


class RuBrandCar(models.Model):
    class Meta:
        verbose_name = _("Перевод марки")
        verbose_name_plural = _("Переводы марок")

    brand = models.CharField(max_length=250, verbose_name='марка')
    ru_brand = models.CharField(max_length=250, verbose_name='перевод марки')

    def __str__(self):
        return f'{self.brand} | {self.ru_brand}'


class RuModelCar(models.Model):
    class Meta:
        verbose_name = _("Перевод модели")
        verbose_name_plural = _("Переводы моделей")

    model = models.CharField(max_length=250, verbose_name='марка')
    ru_model = models.CharField(max_length=250, verbose_name='перевод марки')

    def __str__(self):
        return f'{self.model} | {self.ru_model}'


class RuColorCar(models.Model):
    class Meta:
        verbose_name = _("Перевод цвета")
        verbose_name_plural = _("Переводы цветов")

    color = models.CharField(max_length=250, verbose_name='марка')
    ru_color = models.CharField(max_length=250, verbose_name='перевод марки')

    def __str__(self):
        return f'{self.color} | {self.ru_color}'


class RuTransmissionCar(models.Model):
    class Meta:
        verbose_name = _("Тип КПП")
        verbose_name_plural = _("Типы КПП")

    transmission_ru = models.CharField(max_length=250, verbose_name='Русифицированный тип КПП')
    transmission = models.TextField(verbose_name='Тип КПП', help_text='Через зяпятую')

    def __str__(self):
        return self.transmission_ru


class RuDriveCar(models.Model):
    class Meta:
        verbose_name = _("Тип привода")
        verbose_name_plural = _("Типы приводов")

    drive_ru = models.CharField(max_length=250, verbose_name='Русифицированный тип привода')
    drive = models.TextField(verbose_name='Тип привода', help_text='Через зяпятую')

    def __str__(self):
        return self.drive_ru


class RuEngineCar(models.Model):
    class Meta:
        verbose_name = _("Тип топлива")
        verbose_name_plural = _("Типы топлива")

    engine_ru = models.CharField(max_length=250, verbose_name='Русифицированный тип топлива')
    engine = models.TextField(verbose_name='Тип топлива', help_text='Через зяпятую')

    def __str__(self):
        return self.engine_ru


class RuBodyTypeCar(models.Model):
    class Meta:
        verbose_name = _("Тип кузова")
        verbose_name_plural = _("Типы кузовов")

    body_type_ru = models.CharField(max_length=250, verbose_name='Русифицированный тип кузова')
    body_type = models.TextField(verbose_name='Тип кузова', help_text='Через зяпятую')

    def __str__(self):
        return self.body_type_ru
