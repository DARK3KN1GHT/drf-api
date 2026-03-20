from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from agenda.models import Empresa, Horario
from .forms import AgendamentoForm


def home(request):
    return render(request, "home.html")


def agendar(request):
    if request.method == "POST":
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = AgendamentoForm()

    return render(request, "agendar.html", {"form": form})


def horarios_por_empresa(request):
    empresa_id = request.GET.get("empresa")

    if not empresa_id:
        return JsonResponse({"horarios": []})

    empresa = get_object_or_404(Empresa, id=empresa_id)
    horarios = Horario.objects.filter(empresa=empresa).order_by("horario")

    return JsonResponse({
        "horarios": [
            {
                "id": h.id,
                "horario": h.horario
            }
            for h in horarios
        ]
    })