from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("agendar/", views.agendar, name="agendar"),

    path(
        "api/horarios-por-empresa/",
        views.horarios_por_empresa,
        name="horarios_por_empresa",
    ),

    path(
        "api/cep/<str:cep>/",
        views.consultar_cep_api,
        name="consultar_cep_api",
    ),
]