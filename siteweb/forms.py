from django import forms
from django.core.exceptions import ValidationError
from datetime import date

from agenda.models import Agendamento


class AgendamentoForm(forms.ModelForm):

    class Meta:
        model = Agendamento
        fields = ["nome", "telefone", "data", "horario", "observacoes"]

    def clean(self):
        cleaned_data = super().clean()

        data = cleaned_data.get("data")
        horario = cleaned_data.get("horario")

        # 1️⃣ bloquear datas passadas
        if data and data < date.today():
            raise ValidationError("Não é possível agendar em datas passadas.")

        # 2️⃣ bloquear sábado e domingo
        if data and data.weekday() >= 5:
            raise ValidationError("Atendimento apenas de segunda a sexta.")

        # 3️⃣ limitar a 2 pessoas por horário
        if data and horario:
            qtd = Agendamento.objects.filter(
                data=data,
                horario=horario
            ).count()

            if qtd >= 2:
                raise ValidationError(
                    "Esse horário já atingiu o limite de 2 agendamentos. Escolha outro."
                )

        return cleaned_data