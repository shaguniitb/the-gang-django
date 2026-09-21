from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Route all other URLs to the 'gang' app
    path('', include('gang.urls')),
]
