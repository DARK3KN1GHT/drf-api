from django.db import models

class Horario(models.Model):
    hora = models.TimeField(unique=True)

    def __str__(self):
        return self.hora.strftime("%H:%M")


class Agendamento(models.Model):
    nome = models.CharField(max_length=120)
    data = models.DateField()
    horario = models.ForeignKey(Horario, on_delete=models.PROTECT, related_name="agendamentos")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.data} {self.horario}"