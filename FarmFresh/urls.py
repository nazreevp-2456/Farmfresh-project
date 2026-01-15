from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('', include('store.urls')),      # Home & store pages
    path('users/', include('users.urls')),  # Login, register, dashboards
    path('orders/', include('orders.urls')),
   

]

# Media files (development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)