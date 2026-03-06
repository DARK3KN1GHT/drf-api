from django import forms

from .models import Agendamento, Horario


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ["empresa", "nome", "telefone", "data", "horario", "observacoes"]
        widgets = {
            "empresa": forms.Select(attrs={"class": "select--pretty"}),
            "nome": forms.TextInput(attrs={"placeholder": "Digite seu nome"}),
            "telefone": forms.TextInput(attrs={"placeholder": "(00) 00000-0000"}),
            # IMPORTANTE: texto + flatpickr
            "data": forms.TextInput(attrs={"placeholder": "Selecione uma data", "autocomplete": "off"}),
            "observacoes": forms.Textarea(attrs={"placeholder": "Observações (opcional)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Horário começa vazio; JS busca via /api/horarios-por-empresa/
        self.fields["horario"].queryset = Horario.objects.none()
        self.fields["horario"].empty_label = "Selecione um horário"