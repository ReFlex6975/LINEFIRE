from django.contrib import admin
from .models import Buyer, Polygon

admin.site.register(Buyer)

class PolygonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')