from rest_framework import serializers
from .models import Horario, Agendamento


class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ["id", "hora"]


class AgendamentoSerializer(serializers.ModelSerializer):
    horario_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Agendamento
        fields = ["id", "nome", "data", "horario", "horario_display", "criado_em"]

    def get_horario_display(self, obj):
        return obj.horario.hora.strftime("%H:%M")