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
            "data": forms.TextInput(attrs={"placeholder": "Selecione uma data", "autocomplete": "off"}),
            "horario": forms.Select(attrs={"class": "select--pretty"}),
            "observacoes": forms.Textarea(attrs={"placeholder": "Observações (opcional)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # começa vazio
        self.fields["horario"].queryset = Horario.objects.none()
        self.fields["horario"].empty_label = "Selecione um horário"

        # quando envia o formulário, carrega os horários da empresa escolhida
        if "empresa" in self.data:
            try:
                empresa_id = int(self.data.get("empresa"))
                self.fields["horario"].queryset = Horario.objects.filter(
                    empresa_id=empresa_id
                ).order_by("horario")
            except (ValueError, TypeError):
                pass

        # quando estiver editando um objeto já salvo
        elif self.instance.pk and self.instance.empresa:
            self.fields["horario"].queryset = Horario.objects.filter(
                empresa=self.instance.empresa
            ).order_by("horario")