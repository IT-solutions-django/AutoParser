# Generated by Django 5.1.6 on 2025-02-17 03:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AucCarsPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=500, verbose_name='URL фотографии')),
            ],
            options={
                'verbose_name': 'Фото автомобилей с аукционов',
                'verbose_name_plural': 'Фото автомобилей с аукционов',
            },
        ),
        migrations.CreateModel(
            name='ColorMain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('true_value', models.CharField(max_length=100, null=True, verbose_name='Цвет')),
                ('color', models.CharField(max_length=100, null=True, verbose_name='Цвет RGBA')),
            ],
            options={
                'verbose_name': 'Цвет',
                'verbose_name_plural': 'Цвета',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Страна производителя')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='CountryModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(choices=[('Япония', 'Япония'), ('Китай', 'Китай'), ('Корея', 'Корея'), ('Европа', 'Европа'), ('США', 'США')], max_length=150, verbose_name='Страна производитель')),
                ('brand', models.CharField(max_length=150, verbose_name='Марка авто')),
            ],
            options={
                'verbose_name': 'Бренды авто по странам производителям',
                'verbose_name_plural': 'Бренды авто по странам производителям',
            },
        ),
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Тип топлива',
                'verbose_name_plural': 'Типы топлива',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_value', models.CharField(max_length=100, null=True, verbose_name='Цвет из апи')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_color_api', to='cars.colormain', verbose_name='Цвет')),
            ],
            options={
                'verbose_name': 'Цвет из апи',
                'verbose_name_plural': 'Цвета из апи',
            },
        ),
        migrations.CreateModel(
            name='AucCarsUSA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auc_table', models.CharField(max_length=50, verbose_name='Таблица во внешнем апи')),
                ('lot', models.CharField(max_length=50, verbose_name='Номер лота')),
                ('auc_name', models.CharField(max_length=50, verbose_name='Название аукциона')),
                ('auc_date', models.DateTimeField(verbose_name='Дата аукциона')),
                ('api_id', models.CharField(max_length=50, unique=True, verbose_name='ID автомобиля')),
                ('brand', models.CharField(max_length=50, verbose_name='Бренд')),
                ('model', models.CharField(max_length=50, verbose_name='Модель')),
                ('year', models.IntegerField(verbose_name='Год')),
                ('mileage', models.IntegerField(verbose_name='Пробег')),
                ('price', models.IntegerField(verbose_name='Цена в РФ')),
                ('kuzov', models.CharField(max_length=50, verbose_name='Тип кузова')),
                ('transmission', models.CharField(max_length=50, verbose_name='Тип КПП')),
                ('engine_volume', models.CharField(max_length=50, verbose_name='Объем двигателя')),
                ('drive', models.CharField(max_length=50, verbose_name='Тип привода')),
                ('color', models.CharField(max_length=50, verbose_name='Цвет')),
                ('rate', models.CharField(max_length=5, verbose_name='Рейтинг')),
                ('finish', models.CharField(max_length=50, verbose_name='Цена в валюте экспортера')),
                ('power_volume', models.CharField(blank=True, max_length=30, null=True, verbose_name='Мощность двигателя')),
                ('parsing_date', models.DateField(auto_now=True, verbose_name='Дата парсинга')),
                ('rubber', models.CharField(blank=True, choices=[('Левый руль', 'Левый руль'), ('Правый руль', 'Правый руль')], default='Левый руль', max_length=30, null=True, verbose_name='Руль')),
                ('engine', models.CharField(blank=True, choices=[('Электро', 'Электро'), ('Гибрид', 'Гибрид'), ('Дизель', 'Дизель'), ('Бензин', 'Бензин')], default='Бензин', max_length=30, null=True, verbose_name='Тип двигателя')),
                ('is_active', models.BooleanField()),
                ('photos', models.ManyToManyField(to='cars.auccarsphoto', verbose_name='Фотографии автомобиля')),
                ('brand_country', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.countrymodels', verbose_name='Страна производитель')),
            ],
            options={
                'verbose_name': 'Автомобили США',
                'verbose_name_plural': 'Автомобили США',
            },
        ),
        migrations.CreateModel(
            name='AucCarsKorea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auc_table', models.CharField(max_length=50, verbose_name='Таблица во внешнем апи')),
                ('lot', models.CharField(max_length=50, verbose_name='Номер лота')),
                ('auc_name', models.CharField(max_length=50, verbose_name='Название аукциона')),
                ('auc_date', models.DateTimeField(verbose_name='Дата аукциона')),
                ('api_id', models.CharField(max_length=50, unique=True, verbose_name='ID автомобиля')),
                ('brand', models.CharField(max_length=50, verbose_name='Бренд')),
                ('model', models.CharField(max_length=50, verbose_name='Модель')),
                ('year', models.IntegerField(verbose_name='Год')),
                ('mileage', models.IntegerField(verbose_name='Пробег')),
                ('price', models.IntegerField(verbose_name='Цена в РФ')),
                ('kuzov', models.CharField(max_length=50, verbose_name='Тип кузова')),
                ('transmission', models.CharField(max_length=50, verbose_name='Тип КПП')),
                ('engine_volume', models.CharField(max_length=50, verbose_name='Объем двигателя')),
                ('drive', models.CharField(max_length=50, verbose_name='Тип привода')),
                ('color', models.CharField(max_length=50, verbose_name='Цвет')),
                ('rate', models.CharField(max_length=5, verbose_name='Рейтинг')),
                ('finish', models.CharField(max_length=50, verbose_name='Цена в валюте экспортера')),
                ('power_volume', models.CharField(blank=True, max_length=30, null=True, verbose_name='Мощность двигателя')),
                ('parsing_date', models.DateField(auto_now=True, verbose_name='Дата парсинга')),
                ('rubber', models.CharField(blank=True, choices=[('Левый руль', 'Левый руль'), ('Правый руль', 'Правый руль')], default='Левый руль', max_length=30, null=True, verbose_name='Руль')),
                ('engine', models.CharField(blank=True, choices=[('Электро', 'Электро'), ('Гибрид', 'Гибрид'), ('Дизель', 'Дизель'), ('Бензин', 'Бензин')], default='Бензин', max_length=30, null=True, verbose_name='Тип двигателя')),
                ('is_active', models.BooleanField()),
                ('photos', models.ManyToManyField(to='cars.auccarsphoto', verbose_name='Фотографии автомобиля')),
                ('brand_country', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.countrymodels', verbose_name='Страна производитель')),
            ],
            options={
                'verbose_name': 'Автомобили Корея',
                'verbose_name_plural': 'Автомобили Корея',
            },
        ),
        migrations.CreateModel(
            name='AucCarsJapan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auc_table', models.CharField(max_length=50, verbose_name='Таблица во внешнем апи')),
                ('lot', models.CharField(max_length=50, verbose_name='Номер лота')),
                ('auc_name', models.CharField(max_length=50, verbose_name='Название аукциона')),
                ('auc_date', models.DateTimeField(verbose_name='Дата аукциона')),
                ('api_id', models.CharField(max_length=50, unique=True, verbose_name='ID автомобиля')),
                ('brand', models.CharField(max_length=50, verbose_name='Бренд')),
                ('model', models.CharField(max_length=50, verbose_name='Модель')),
                ('year', models.IntegerField(verbose_name='Год')),
                ('mileage', models.IntegerField(verbose_name='Пробег')),
                ('price', models.IntegerField(verbose_name='Цена в РФ')),
                ('kuzov', models.CharField(max_length=50, verbose_name='Тип кузова')),
                ('transmission', models.CharField(max_length=50, verbose_name='Тип КПП')),
                ('engine_volume', models.CharField(max_length=50, verbose_name='Объем двигателя')),
                ('drive', models.CharField(max_length=50, verbose_name='Тип привода')),
                ('color', models.CharField(max_length=50, verbose_name='Цвет')),
                ('rate', models.CharField(max_length=5, verbose_name='Рейтинг')),
                ('finish', models.CharField(max_length=50, verbose_name='Цена в валюте экспортера')),
                ('power_volume', models.CharField(blank=True, max_length=30, null=True, verbose_name='Мощность двигателя')),
                ('parsing_date', models.DateField(auto_now=True, verbose_name='Дата парсинга')),
                ('rubber', models.CharField(blank=True, choices=[('Левый руль', 'Левый руль'), ('Правый руль', 'Правый руль')], default='Левый руль', max_length=30, null=True, verbose_name='Руль')),
                ('engine', models.CharField(blank=True, choices=[('Электро', 'Электро'), ('Гибрид', 'Гибрид'), ('Дизель', 'Дизель'), ('Бензин', 'Бензин')], default='Бензин', max_length=30, null=True, verbose_name='Тип двигателя')),
                ('is_active', models.BooleanField()),
                ('photos', models.ManyToManyField(to='cars.auccarsphoto', verbose_name='Фотографии автомобиля')),
                ('brand_country', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.countrymodels', verbose_name='Страна производитель')),
            ],
            options={
                'verbose_name': 'Автомобили Япония',
                'verbose_name_plural': 'Автомобили Япония',
            },
        ),
        migrations.CreateModel(
            name='AucCarsEurope',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auc_table', models.CharField(max_length=50, verbose_name='Таблица во внешнем апи')),
                ('lot', models.CharField(max_length=50, verbose_name='Номер лота')),
                ('auc_name', models.CharField(max_length=50, verbose_name='Название аукциона')),
                ('auc_date', models.DateTimeField(verbose_name='Дата аукциона')),
                ('api_id', models.CharField(max_length=50, unique=True, verbose_name='ID автомобиля')),
                ('brand', models.CharField(max_length=50, verbose_name='Бренд')),
                ('model', models.CharField(max_length=50, verbose_name='Модель')),
                ('year', models.IntegerField(verbose_name='Год')),
                ('mileage', models.IntegerField(verbose_name='Пробег')),
                ('price', models.IntegerField(verbose_name='Цена в РФ')),
                ('kuzov', models.CharField(max_length=50, verbose_name='Тип кузова')),
                ('transmission', models.CharField(max_length=50, verbose_name='Тип КПП')),
                ('engine_volume', models.CharField(max_length=50, verbose_name='Объем двигателя')),
                ('drive', models.CharField(max_length=50, verbose_name='Тип привода')),
                ('color', models.CharField(max_length=50, verbose_name='Цвет')),
                ('rate', models.CharField(max_length=5, verbose_name='Рейтинг')),
                ('finish', models.CharField(max_length=50, verbose_name='Цена в валюте экспортера')),
                ('power_volume', models.CharField(blank=True, max_length=30, null=True, verbose_name='Мощность двигателя')),
                ('parsing_date', models.DateField(auto_now=True, verbose_name='Дата парсинга')),
                ('rubber', models.CharField(blank=True, choices=[('Левый руль', 'Левый руль'), ('Правый руль', 'Правый руль')], default='Левый руль', max_length=30, null=True, verbose_name='Руль')),
                ('engine', models.CharField(blank=True, choices=[('Электро', 'Электро'), ('Гибрид', 'Гибрид'), ('Дизель', 'Дизель'), ('Бензин', 'Бензин')], default='Бензин', max_length=30, null=True, verbose_name='Тип двигателя')),
                ('is_active', models.BooleanField()),
                ('photos', models.ManyToManyField(to='cars.auccarsphoto', verbose_name='Фотографии автомобиля')),
                ('brand_country', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.countrymodels', verbose_name='Страна производитель')),
            ],
            options={
                'verbose_name': 'Автомобили Европа',
                'verbose_name_plural': 'Автомобили Европа',
            },
        ),
        migrations.CreateModel(
            name='AucCarsChina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auc_table', models.CharField(max_length=50, verbose_name='Таблица во внешнем апи')),
                ('lot', models.CharField(max_length=50, verbose_name='Номер лота')),
                ('auc_name', models.CharField(max_length=50, verbose_name='Название аукциона')),
                ('auc_date', models.DateTimeField(verbose_name='Дата аукциона')),
                ('api_id', models.CharField(max_length=50, unique=True, verbose_name='ID автомобиля')),
                ('brand', models.CharField(max_length=50, verbose_name='Бренд')),
                ('model', models.CharField(max_length=50, verbose_name='Модель')),
                ('year', models.IntegerField(verbose_name='Год')),
                ('mileage', models.IntegerField(verbose_name='Пробег')),
                ('price', models.IntegerField(verbose_name='Цена в РФ')),
                ('kuzov', models.CharField(max_length=50, verbose_name='Тип кузова')),
                ('transmission', models.CharField(max_length=50, verbose_name='Тип КПП')),
                ('engine_volume', models.CharField(max_length=50, verbose_name='Объем двигателя')),
                ('drive', models.CharField(max_length=50, verbose_name='Тип привода')),
                ('color', models.CharField(max_length=50, verbose_name='Цвет')),
                ('rate', models.CharField(max_length=5, verbose_name='Рейтинг')),
                ('finish', models.CharField(max_length=50, verbose_name='Цена в валюте экспортера')),
                ('power_volume', models.CharField(blank=True, max_length=30, null=True, verbose_name='Мощность двигателя')),
                ('parsing_date', models.DateField(auto_now=True, verbose_name='Дата парсинга')),
                ('rubber', models.CharField(blank=True, choices=[('Левый руль', 'Левый руль'), ('Правый руль', 'Правый руль')], default='Левый руль', max_length=30, null=True, verbose_name='Руль')),
                ('engine', models.CharField(blank=True, choices=[('Электро', 'Электро'), ('Гибрид', 'Гибрид'), ('Дизель', 'Дизель'), ('Бензин', 'Бензин')], default='Бензин', max_length=30, null=True, verbose_name='Тип двигателя')),
                ('is_active', models.BooleanField()),
                ('photos', models.ManyToManyField(to='cars.auccarsphoto', verbose_name='Фотографии автомобиля')),
                ('brand_country', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.countrymodels', verbose_name='Страна производитель')),
            ],
            options={
                'verbose_name': 'Автомобили Китай',
                'verbose_name_plural': 'Автомобили Китай',
            },
        ),
    ]
