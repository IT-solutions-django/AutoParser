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


@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    pass
   
   
@admin.register(AucCars)
class AucCarsAdmin(admin.ModelAdmin):
    pass


@admin.register(RuBrandCar)
class RuBrandCarAdmin(admin.ModelAdmin):
    pass


@admin.register(RuModelCar)
class RuModelCarAdmin(admin.ModelAdmin):
    pass


@admin.register(RuColorCar)
class RuColorCarAdmin(admin.ModelAdmin):
    pass


@admin.register(RuTransmissionCar)
class RuTransmissionCarAdmin(admin.ModelAdmin):
    pass


@admin.register(RuDriveCar)
class RuDriveCarAdmin(admin.ModelAdmin):
    pass


@admin.register(RuEngineCar)
class RuEngineCarAdmin(admin.ModelAdmin):
    pass


@admin.register(RuBodyTypeCar)
class RuBodyTypeCarAdmin(admin.ModelAdmin):
    pass



