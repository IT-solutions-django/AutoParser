from django.urls import path
from .views import *


app_name = 'cars'


urlpatterns = [
    path('parse-kcar/', ParseKcarView.as_view()),

    path('load-brands/', LoadMarksView.as_view()),
    path('delete-brands/', DeleteMarksView.as_view()),

    path('translation-mark/', TranslateMark.as_view()),
    path('translation-model/', TranslateModel.as_view()),
    path('translation-color/', TranslateColor.as_view()),

    path('get-brands/', get_brands, name='get-brands'),
    path('get-models/', get_models, name='get-models'),
    path('get-cars/', get_filter_cars, name='get-cars'),
    path('get-all-models/', get_models_all, name='get-all-models'),
    path('get-car/', get_car, name='get-car'),
]