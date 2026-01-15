from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'farmer')
    list_filter = ('farmer',)
    search_fields = ('name',)

