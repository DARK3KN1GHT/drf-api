from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from rest_framework import filters, generics, viewsets
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .forms import AgendamentoForm
from .models import Horario, Agendamento
from .serializers import HorarioSerializer, AgendamentoSerializer
from .permissions import IsAdminForDeleteOtherwiseAuthenticatedOrReadOnly


# =========================================================
# 🔹 HTML
# =========================================================
def home(request):
    return render(request, "home.html")


def agendar(request):
    if request.method == "POST":
        form = AgendamentoForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)

            data_str = (request.POST.get("data") or "").strip()

            try:
                obj.data = datetime.strptime(
                    data_str,
                    "%d/%m/%Y"
                ).date()

            except ValueError:
                form.add_error(
                    "data",
                    "Data inválida."
                )

                return render(
                    request,
                    "agendar.html",
                    {"form": form}
                )

            if obj.data < timezone.localdate():
                form.add_error(
                    "data",
                    "Não é permitido data passada."
                )

                return render(
                    request,
                    "agendar.html",
                    {"form": form}
                )

            obj.save()

            return redirect("agendar")

    else:
        form = AgendamentoForm()

    return render(
        request,
        "agendar.html",
        {"form": form}
    )


def horarios_por_empresa(request):
    empresa_id = request.GET.get("empresa_id")

    qs = Horario.objects.filter(
        empresa_id=empresa_id
    ).order_by("horario")

    horarios = []

    for h in qs:
        horario_txt = h.horario.strftime("%H:%M")

        horarios.append({
            "id": h.id,
            "horario": horario_txt
        })

    return JsonResponse({
        "horarios": horarios
    })


# =========================================================
# 🔹 API DRF
# =========================================================

# Horários são públicos
class HorarioListAPIView(generics.ListAPIView):
    queryset = Horario.objects.all().order_by("horario")
    serializer_class = HorarioSerializer
    permission_classes = [AllowAny]


# Agendamentos
class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all().order_by("-criado_em")
    serializer_class = AgendamentoSerializer

    # Permissões:
    # GET / HEAD / OPTIONS -> público
    # POST / PUT / PATCH   -> usuário autenticado
    # DELETE               -> somente staff/admin
    permission_classes = [
        IsAdminForDeleteOtherwiseAuthenticatedOrReadOnly
    ]

    # Filtros, busca e ordenação
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Filtros exatos
    filterset_fields = [
        "empresa",
        "data",
        "nome",
    ]

    # Busca textual
    search_fields = [
        "nome",
        "telefone",
        "observacoes",
    ]

    # Campos permitidos para ordenação
    ordering_fields = [
        "data",
        "criado_em",
        "nome",
    ]

    # Ordenação padrão
    ordering = [
        "-criado_em"
    ]