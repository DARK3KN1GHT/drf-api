from django.contrib import admin
from .models import Empresa, Horario, Agendamento


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "telefone")
    search_fields = ("nome", "telefone")


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ("id", "empresa", "horario")
    list_filter = ("empresa",)
    search_fields = ("empresa__nome", "horario")


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "empresa", "nome", "telefone", "data", "horario", "criado_em")
    list_filter = ("empresa", "data")
    search_fields = ("nome", "telefone", "empresa__nome", "horario__horario")