from django.urls import path

from . import views

app_name = 'weather_rest'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
