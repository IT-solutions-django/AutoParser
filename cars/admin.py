from django.contrib import admin
from .models import *


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass

@admin.register(Color)
class ColoryAdmin(admin.ModelAdmin):
    search_fields = ('api_value', )

@admin.register(ColorMain)
class ColorMainAdmin(admin.ModelAdmin):
    search_fields = ('value', )


@admin.register(CountryModels)
class CountryModelsAdmin(admin.ModelAdmin):
    pass

@admin.register(AucCarsJapan)
class AucCarsJapanAdmin(admin.ModelAdmin):
    pass
   
@admin.register(AucCarsChina)
class AucCarsChinaAdmin(admin.ModelAdmin):
    pass
   

@admin.register(AucCarsKorea)
class AucCarsKoreaAdmin(admin.ModelAdmin):
    pass
   

@admin.register(AucCarsEurope)
class AucCarsEuropeAdmin(admin.ModelAdmin):
    pass


@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    pass
   
   
@admin.register(AucCarsRest)
class AucCarsRestAdmin(admin.ModelAdmin):
    pass

