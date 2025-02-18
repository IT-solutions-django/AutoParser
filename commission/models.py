from django.db import models
from cars.models import Country


class Commission(models.Model):
    delivery = models.PositiveIntegerField(
        verbose_name="доставка в РФ",
        help_text="в ваоюте",
    )
    commission_broker = models.PositiveIntegerField(
        verbose_name="Брокер",
        help_text="в рублях",
    )
    commission = models.PositiveIntegerField(
        verbose_name="Комиссия", help_text="в рублях"
    )
    japan_sanction_delivery = models.PositiveIntegerField(
        verbose_name="Доставка санкционного авто",
        help_text="в валюте страны экспортера",
        blank=True,
        null=True,
    )
    japan_sanction_percent = models.PositiveIntegerField(
        verbose_name="Процент комиссии санкционных авто",
        help_text="в процентах",
        blank=True,
        null=True,
    )

    japan_insurance = models.PositiveIntegerField(
        verbose_name="Страховка",
        help_text="в валюте страны экспортера",
        blank=True,
        null=True,
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE,
        verbose_name="Страна экспортер",
        default=None
    )

    table = models.CharField('Таблица в API', max_length=50)

    class Meta:
        verbose_name = "комиссия"
        verbose_name_plural = "комиссии"
        ordering = ("country",)

    def __str__(self):
        return f"Комиссия из {self.country}"
