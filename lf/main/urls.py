from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('statistics', views.statistics, name='statistics'),
    path('polygons', views.polygons, name='polygons'),
    path('scenarios', views.scenarios, name='scenarios'),
    path('cabinet', views.cabinet, name='cabinet'),
    path('contact/', views.contact_form, name='contact'),  # Путь для обработки формы
]