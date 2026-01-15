from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),

    # ✅ CUSTOMER
    path('my-orders/', views.my_orders, name='my_orders'),

    # ✅ FARMER (ONLY ONE URL — VERY IMPORTANT)
    path('farmer-orders/', views.farmer_orders, name='farmer_orders'),
    path('farmer/deliver/<int:order_id>/', views.deliver_order, name='deliver_order'),
    path('farmer/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),

]
