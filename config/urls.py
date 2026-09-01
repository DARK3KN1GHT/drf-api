from django.contrib import admin
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from agenda import views


router = DefaultRouter()

router.register(
    r"agendamentos",
    views.AgendamentoViewSet,
    basename="agendamentos",
)


urlpatterns = [
    path("admin/", admin.site.urls),

    # API pública para listar os horários
    path(
        "api/horarios/",
        views.HorarioListAPIView.as_view(),
        name="horarios-list",
    ),

    # Páginas HTML do sistema
    path("", include("siteweb.urls")),

    # Rotas automáticas do Django REST Framework
    path("api/", include(router.urls)),

    # Autenticação JWT
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # Documentação da API
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="api_schema",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api_schema"),
        name="api_docs",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="api_schema"),
        name="api_redoc",
    ),
    path(
        "api/cep/<str:cep>/",
        views.consultar_cep_api,
        name="consultar_cep_api",
    ),
]