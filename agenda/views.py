from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import AgendamentoForm
from .models import Horario


def home(request):
    return render(request, "home.html")


def agendar(request):
    if request.method == "POST":
        form = AgendamentoForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)

            # data vem como "dd/mm/yyyy" (flatpickr -> input text)
            data_str = (request.POST.get("data") or "").strip()
            try:
                obj.data = datetime.strptime(data_str, "%d/%m/%Y").date()
            except ValueError:
                form.add_error("data", "Data inválida. Selecione pelo calendário.")
                return render(request, "agendar.html", {"form": form})

            # trava datas passadas no backend também
            if obj.data < timezone.localdate():
                form.add_error("data", "Não é permitido agendar em datas passadas.")
                return render(request, "agendar.html", {"form": form})

            obj.save()
            return redirect("agendar")
    else:
        form = AgendamentoForm()

    return render(request, "agendar.html", {"form": form})


def horarios_por_empresa(request):
    empresa_id = request.GET.get("empresa_id")
    qs = Horario.objects.filter(empresa_id=empresa_id).order_by("horario")

    horarios = []
    for h in qs:
        # Seu model usa CharField -> pode vir "07:00:00" ou "07:00"
        if isinstance(h.horario, str):
            horario_txt = h.horario.strip()[:5]  # garante HH:MM
        else:
            # se algum dia virar TimeField, continua funcionando
            horario_txt = h.horario.strftime("%H:%M")

        horarios.append({"id": h.id, "horario": horario_txt})

    return JsonResponse({"horarios": horarios})