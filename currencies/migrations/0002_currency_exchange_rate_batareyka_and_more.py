# Generated by Django 5.1.6 on 2025-04-15 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='exchange_rate_batareyka',
            field=models.FloatField(default=0.0, verbose_name='Курс по батарейке'),
        ),
        migrations.AddField(
            model_name='currency',
            name='exchange_rate_cbr',
            field=models.FloatField(default=0.0, verbose_name='Курс по Центробанку РФ'),
        ),
        migrations.AddField(
            model_name='currency',
            name='exchange_rate_tks',
            field=models.FloatField(default=0.0, verbose_name='Курс по ТКС'),
        ),
    ]
