from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('upload/', views.upload_file, name='upload'),
    path('edit/<int:file_id>/', views.edit_gamer_view, name='edit_gamer'),
    path('success/', views.success_view, name='success'),
    path('files/', views.file_list_view, name='file_list'),
    path('delete/<int:file_id>/', views.delete_file_view, name='delete_file'),
    path('files/<int:file_id>/stats/', views.file_stats_view, name='file_stats'),
]