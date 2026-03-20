from django import forms
from agenda.models import Agendamento, Empresa, Horario


class AgendamentoForm(forms.ModelForm):
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),
        empty_label="Selecione uma empresa",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    horario = forms.ModelChoiceField(
        queryset=Horario.objects.none(),
        empty_label="Selecione um horário",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    data = forms.DateField(
        widget=forms.DateInput(attrs={
            "class": "form-control",
            "placeholder": "Selecione uma data",
            "autocomplete": "off",
        })
    )

    class Meta:
        model = Agendamento
        fields = ["empresa", "nome", "telefone", "data", "horario", "observacoes"]
        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Digite seu nome",
            }),
            "telefone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "(00) 00000-0000",
            }),
            "observacoes": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Observações (opcional)",
                "rows": 5,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "empresa" in self.data:
            try:
                empresa_id = int(self.data.get("empresa"))
                self.fields["horario"].queryset = Horario.objects.filter(
                    empresa_id=empresa_id
                ).order_by("horario")
            except (ValueError, TypeError):
                self.fields["horario"].queryset = Horario.objects.none()
        elif self.instance.pk and self.instance.empresa:
            self.fields["horario"].queryset = Horario.objects.filter(
                empresa=self.instance.empresa
            ).order_by("horario")
        else:
            self.fields["horario"].queryset = Horario.objects.none()