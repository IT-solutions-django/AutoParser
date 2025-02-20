from django.urls import path
from .views import *


app_name = 'cars'


urlpatterns = [
    path('fetch-test-data/', FetchTestData.as_view()),

    path('load-brands/', LoadMarksView.as_view()),
    path('delete-brands/', DeleteMarksView.as_view()),
]