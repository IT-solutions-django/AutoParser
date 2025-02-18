from django.contrib import admin
from .models import Commission 


@admin.register(Commission) 
class CommissionAdmin(admin.ModelAdmin): 
    pass