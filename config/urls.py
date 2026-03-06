from django.contrib import admin
from django.urls import path

from agenda import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("agendar/", views.agendar, name="agendar"),
    path("api/horarios-por-empresa/", views.horarios_por_empresa, name="horarios_por_empresa"),
]