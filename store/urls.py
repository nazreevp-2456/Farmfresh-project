from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Farmer URLs
    path('farmer/dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('farmer/products/', views.my_products, name='my_products'),
    path('farmer/add-product/', views.add_product, name='add_product'),

    # Customer URLs
    path('products/', views.browse_products, name='browse_products'),
]
