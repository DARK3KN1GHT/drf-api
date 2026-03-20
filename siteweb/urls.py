from django.urls import path
from .views import home, agendar, horarios_por_empresa

urlpatterns = [
    path("", home, name="home"),
    path("agendar/", agendar, name="agendar"),
    path("api/horarios-por-empresa/", horarios_por_empresa, name="horarios_por_empresa"),
]