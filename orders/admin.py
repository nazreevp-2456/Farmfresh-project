from django.contrib import admin
from .models import Order, Cart, CartItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'quantity', 'status', 'ordered_at')
    list_filter = ('status',)
    search_fields = ('customer__username', 'product__name')

admin.site.register(Cart)
admin.site.register(CartItem)
