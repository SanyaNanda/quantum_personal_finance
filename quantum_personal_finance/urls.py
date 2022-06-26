"""quantum_personal_finance URL Configuration"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authenticate.urls', namespace='authenticate')),
    path('finances/', include('finances.urls', namespace='finances')),
]
