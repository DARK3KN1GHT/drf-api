from rest_framework import generics
from .models import Horario, Agendamento
from .serializers import HorarioSerializer, AgendamentoSerializer


class HorarioListView(generics.ListAPIView):
    queryset = Horario.objects.all().order_by("hora")
    serializer_class = HorarioSerializer


class AgendamentoListCreateView(generics.ListCreateAPIView):
    queryset = Agendamento.objects.all().order_by("-criado_em")
    serializer_class = AgendamentoSerializer


class AgendamentoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer