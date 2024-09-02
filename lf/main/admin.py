from django.contrib import admin
from .models import Polygon, CustomUser, Scenario, Section, Equipment


class PolygonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


admin.site.register(Polygon, PolygonAdmin)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type')


admin.site.register(CustomUser, CustomUserAdmin)


class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_url')


admin.site.register(Scenario, ScenarioAdmin)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')


admin.site.register(Section, SectionAdmin)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')


admin.site.register(Equipment, EquipmentAdmin)
