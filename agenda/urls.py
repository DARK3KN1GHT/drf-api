from django.urls import path
from .views import HorarioListView, AgendamentoListCreateView, AgendamentoDetailView

urlpatterns = [
    path("horarios/", HorarioListView.as_view(), name="horarios-list"),
    path("agendamentos/", AgendamentoListCreateView.as_view(), name="agendamentos-list"),
    path("agendamentos/<int:pk>/", AgendamentoDetailView.as_view(), name="agendamentos-detail"),
]