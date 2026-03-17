from rest_framework import serializers
from .models import Horario, Agendamento


class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ["id", "empresa", "horario"]


class AgendamentoSerializer(serializers.ModelSerializer):
    horario_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Agendamento
        fields = [
            "id",
            "empresa",
            "nome",
            "telefone",
            "data",
            "horario",
            "horario_display",
            "observacoes",
            "criado_em",
        ]
        read_only_fields = ["criado_em", "horario_display"]

    def validate(self, data):
        empresa = data.get("empresa")
        data_agendamento = data.get("data")
        horario = data.get("horario")

        if Agendamento.objects.filter(
            empresa=empresa,
            data=data_agendamento,
            horario=horario
        ).exists():
            raise serializers.ValidationError(
                "Este horário já está ocupado para essa empresa."
            )

        return data

    def get_horario_display(self, obj):
        if obj.horario and obj.horario.horario:
            return str(obj.horario.horario)[:5]
        return None