from django.urls import path, include
from . import views
from .views import LoginView, PolygonListView, PolygonDetailView, PolygonCreateView, PolygonUpdateView, PolygonDeleteView
from django.contrib.auth import views as auth_views


app_name = 'main'  # Пространство имен для приложения


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('statistics/', views.statistics, name='statistics'),
    path('polygons/', PolygonListView.as_view(), name='polygons'),
    path('scenarios/', views.scenarios, name='scenarios'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('profile/', views.profile_view, name='profile'),  # Путь для профиля
    path('accounts/', include('django.contrib.auth.urls')),  # Встроенные URL авторизации
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('<int:pk>/', PolygonDetailView.as_view(), name='polygon-detail'),
    path('add/', PolygonCreateView.as_view(), name='polygon-add'),
    path('polygons/<int:pk>/edit/', PolygonUpdateView.as_view(), name='polygon-edit'),
    path('<int:pk>/delete/', PolygonDeleteView.as_view(), name='polygon-delete'),
]
