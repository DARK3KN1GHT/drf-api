from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

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
        empresa = data.get(
            "empresa",
            getattr(self.instance, "empresa", None)
        )

        data_agendamento = data.get(
            "data",
            getattr(self.instance, "data", None)
        )

        horario = data.get(
            "horario",
            getattr(self.instance, "horario", None)
        )

        qs = Agendamento.objects.filter(
            empresa=empresa,
            data=data_agendamento,
            horario=horario,
        )

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.count() >= 2:
            raise serializers.ValidationError(
                "Esse horário já atingiu o limite de 2 agendamentos."
            )

        return data
    @extend_schema_field(serializers.CharField())
    def get_horario_display(self, obj):
        if obj.horario and obj.horario.horario:
            return str(obj.horario.horario)[:5]
        return None