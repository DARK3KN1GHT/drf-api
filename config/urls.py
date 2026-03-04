from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('siteweb.urls')),      # Site HTML
    path('api/', include('agenda.urls')),   # API
    path('admin/', admin.site.urls),
]