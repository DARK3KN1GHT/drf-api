from django.shortcuts import render, redirect
from django.contrib import messages
from agenda.models import Horario, Agendamento

def home(request):
    return render(request, "home.html")

def agendar(request):
    horarios = Horario.objects.all().order_by("hora")

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        data = request.POST.get("data", "").strip()
        horario_id = request.POST.get("horario", "").strip()

        if not nome or not data or not horario_id:
            messages.error(request, "Preencha todos os campos para concluir o agendamento.")
            return render(request, "agendar.html", {"horarios": horarios})

        Agendamento.objects.create(
            nome=nome,
            data=data,
            horario_id=horario_id
        )

        return redirect("sucesso")

    return render(request, "agendar.html", {"horarios": horarios})

def sucesso(request):
    return render(request, "sucesso.html")