from django.urls import path
from .views import *


app_name = 'cars'


urlpatterns = [
    path("api/cars/", AucCarsListView.as_view(), name="auc-cars-list"),

    path('fetch-test-data/', FetchTestData.as_view()),
]