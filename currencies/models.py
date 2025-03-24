from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        choices = (
            ("USD", "USD"),
            ("EUR", "EUR"),
            ("JPY", "JPY"),
            ("CNY", "CNY"),
            ("KRW", "KRW"),
            ("JPY_crypto", "JPY_crypto"),
            ("CNY_crypto", "CNY_crypto"),
            ("KRW_crypto", "KRW_crypto"),
        )
    )

    exchange_rate = models.FloatField(
        default=0.0,
        verbose_name=_("Курс"),
    )

    exchange_rate_cbr = models.FloatField(
        default=0.0, 
        verbose_name='Курс по Центробанку РФ'
    )

    exchange_rate_tks = models.FloatField(
        default=0.0, 
        verbose_name='Курс по ТКС'
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.name} {self.exchange_rate} {self.updated_at}'
    
    @staticmethod
    def get_jpy() -> 'Currency': 
        return Currency.objects.filter(name='JPY').first()
    
    @staticmethod
    def get_cny() -> 'Currency': 
        return Currency.objects.filter(name='CNY').first()
    
    @staticmethod
    def get_krw() -> 'Currency': 
        return Currency.objects.filter(name='KRW').first()
    
    @staticmethod
    def get_usd() -> 'Currency': 
        return Currency.objects.filter(name='USD').first()
    
    @staticmethod
    def get_eur() -> 'Currency': 
        return Currency.objects.filter(name='EUR').first()