from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from agenda import views

router = DefaultRouter()
router.register(r"agendamentos", views.AgendamentoViewSet, basename="agendamentos")

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("siteweb.urls")),

    path("api/", include(router.urls)),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/schema/", SpectacularAPIView.as_view(), name="api_schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="api_schema"), name="api_docs"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="api_schema"), name="api_redoc"),
]