from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rolodex.urls')),  # Include your app's URLs
    # Other URL patterns
]
