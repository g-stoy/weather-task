from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('get_city_weather/', views.get_current_city),
    path('refresh/', views.refresh)
]