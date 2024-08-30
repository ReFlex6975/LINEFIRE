from django.urls import path, include
from . import views
from .views import PolygonListView, PolygonDetailView, PolygonCreateView, PolygonUpdateView, PolygonDeleteView, \
    ScenarioListView, ScenarioCreateView, ScenarioUpdateView, ScenarioDeleteView, register_manager, register_player, \
    player_list, section_list, add_section, edit_section, delete_section, player_profile
from django.contrib.auth import views as auth_views

app_name = 'main'

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('statistics/', views.statistics, name='statistics'),
    path('polygons/', PolygonListView.as_view(), name='polygons'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('profile/', views.profile_view, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('<int:pk>/', PolygonDetailView.as_view(), name='polygon-detail'),
    path('add/', PolygonCreateView.as_view(), name='polygon-add'),
    path('polygons/<int:pk>/edit/', PolygonUpdateView.as_view(), name='polygon-edit'),
    path('<int:pk>/delete/', PolygonDeleteView.as_view(), name='polygon-delete'),
    path('scenarios/', ScenarioListView.as_view(), name='scenario-list'),
    path('scenarios/add/', ScenarioCreateView.as_view(), name='scenario-create'),
    path('scenarios/<int:pk>/edit/', ScenarioUpdateView.as_view(), name='scenario-edit'),
    path('scenarios/<int:pk>/delete/', ScenarioDeleteView.as_view(), name='scenario-delete'),
    path('register/manager/', register_manager, name='register_manager'),
    path('register/player/', register_player, name='register_player'),
    path('players/', player_list, name='player_list'),
    path('sections/', section_list, name='section_list'),
    path('sections/add/', add_section, name='add_section'),
    path('sections/edit/<int:pk>/', edit_section, name='edit_section'),
    path('sections/delete/<int:pk>/', delete_section, name='delete_section'),
    path('player/<int:pk>/', player_profile, name='player_profile'),
]
