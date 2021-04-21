from django.urls import path

from . import views

app_name = 'weather_rest'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new-session/', views.NewSessionView.as_view(), name='new-session'),
    path('remove-city/', views.RemoveCity.as_view(), name='remove-city'),
]
