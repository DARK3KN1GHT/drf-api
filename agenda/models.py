from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Empresa(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Horario(models.Model):
    """
    Horários disponíveis por empresa.
    Ex.: Empresa A -> 08:00, 09:00...
    """
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="horarios"
    )
    horario = models.CharField(max_length=5)  # "08:00", "09:00"...

    class Meta:
        # impede repetir o mesmo horário na mesma empresa
        constraints = [
            models.UniqueConstraint(
                fields=["empresa", "horario"],
                name="uniq_horario_por_empresa"
            )
        ]
        ordering = ["empresa__nome", "horario"]

    def clean(self):
        # garante formato HH:00 (minutos sempre 00)
        # Aceita 00:00 até 23:00
        try:
            hh, mm = self.horario.split(":")
            hh = int(hh)
            mm = int(mm)
        except Exception:
            raise ValidationError({"horario": "Use o formato HH:00. Ex.: 08:00"})

        if not (0 <= hh <= 23):
            raise ValidationError({"horario": "Hora inválida (00 a 23)."})
        if mm != 0:
            raise ValidationError({"horario": "Minutos devem ser 00. Ex.: 14:00"})

        # normaliza para sempre ter 2 dígitos
        self.horario = f"{hh:02d}:00"

    def save(self, *args, **kwargs):
        self.full_clean()  # aplica clean() antes de salvar
        super().save(*args, **kwargs)

    def __str__(self):
        # No select do formulário queremos apenas o horário (HH:00)
        return str(self.horario)


class Agendamento(models.Model):
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="agendamentos",
    )

    # Horário escolhido (já pertence a uma empresa)
    horario = models.ForeignKey(
        Horario,
        on_delete=models.PROTECT,
        related_name="agendamentos",
    )

    data = models.DateField()
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)
    observacoes = models.TextField(blank=True)

    criado_em = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-data", "horario__horario", "nome"]
        indexes = [
            models.Index(fields=["empresa", "data", "horario"]),
        ]

    def clean(self):
        # 1) impede escolher um horario que não é da empresa selecionada
        if self.empresa_id and self.horario_id:
            if self.horario.empresa_id != self.empresa_id:
                raise ValidationError({"horario": "Esse horário não pertence à empresa selecionada."})

        # 2) regra: no máximo 2 pessoas por horário (empresa + data + horário)
        if self.empresa_id and self.horario_id and self.data:
            qs = Agendamento.objects.filter(
                empresa_id=self.empresa_id,
                horario_id=self.horario_id,
                data=self.data,
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)

            if qs.count() >= 2:
                raise ValidationError("Esse horário já atingiu o limite de 2 agendamentos.")

    def save(self, *args, **kwargs):
        self.full_clean()  # aplica validações do clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} - {self.empresa.nome} - {self.data} {self.horario.horario}"