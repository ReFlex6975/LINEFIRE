from django.contrib import admin
from .models import Polygon, CustomUser


class PolygonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


admin.site.register(Polygon, PolygonAdmin)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type')


admin.site.register(CustomUser, CustomUserAdmin)
