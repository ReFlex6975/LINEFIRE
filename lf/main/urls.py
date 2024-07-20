from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('statistics', views.statistics, name='statistics'),
    path('polygons', views.polygons, name='polygons'),
    path('scenarios', views.scenarios, name='scenarios'),
    path('about', views.about, name='about'),
    path('cabinet', views.cabinet, name='cabinet'),
]