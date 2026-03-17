from datetime import date

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Empresa, Horario, Agendamento


class EmpresaHorarioModelTests(APITestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nome="Empresa A",
            telefone="(62) 99999-9999"
        )

        self.horario = Horario.objects.create(
            empresa=self.empresa,
            horario="08:00"
        )

    def test_cria_empresa_corretamente(self):
        self.assertEqual(self.empresa.nome, "Empresa A")
        self.assertEqual(self.empresa.telefone, "(62) 99999-9999")

    def test_cria_horario_corretamente(self):
        self.assertEqual(self.horario.empresa.nome, "Empresa A")
        self.assertEqual(self.horario.horario, "08:00")


class HorarioAPITests(APITestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nome="Empresa A",
            telefone="(62) 99999-9999"
        )

        Horario.objects.create(empresa=self.empresa, horario="08:00")
        Horario.objects.create(empresa=self.empresa, horario="09:00")

    def test_lista_horarios(self):
        url = "/api/horarios/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if "results" in response.data:
            self.assertEqual(len(response.data["results"]), 2)
        else:
            self.assertEqual(len(response.data), 2)


class AgendamentoAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teste_lista",
            password="123456"
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        self.empresa = Empresa.objects.create(
            nome="Empresa A",
            telefone="(62) 99999-9999"
        )

        self.horario = Horario.objects.create(
            empresa=self.empresa,
            horario="10:00"
        )

        Agendamento.objects.create(
            empresa=self.empresa,
            nome="Carlos",
            telefone="(62) 98888-7777",
            data=date(2026, 3, 31),
            horario=self.horario,
            observacoes="Teste automático"
        )

    def test_lista_agendamentos(self):
        url = "/api/agendamentos/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if "count" in response.data:
            self.assertEqual(response.data["count"], 1)
            self.assertEqual(response.data["results"][0]["nome"], "Carlos")
            self.assertEqual(response.data["results"][0]["horario_display"], "10:00")
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]["nome"], "Carlos")
            self.assertEqual(response.data[0]["horario_display"], "10:00")


class AgendamentoCreateAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teste_create",
            password="123456"
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        self.empresa = Empresa.objects.create(
            nome="Empresa B",
            telefone="(62) 97777-6666"
        )

        self.horario = Horario.objects.create(
            empresa=self.empresa,
            horario="14:00"
        )

    def test_cria_agendamento_via_api(self):
        url = "/api/agendamentos/"
        payload = {
            "empresa": self.empresa.id,
            "nome": "João",
            "telefone": "(62) 99999-1111",
            "data": "2026-04-10",
            "horario": self.horario.id,
            "observacoes": "Teste de criação"
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Agendamento.objects.count(), 1)
        self.assertEqual(Agendamento.objects.first().nome, "João")


class AgendamentoRegraNegocioTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teste_regra",
            password="123456"
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        self.empresa = Empresa.objects.create(
            nome="Empresa X",
            telefone="(62) 90000-0000"
        )

        self.horario = Horario.objects.create(
            empresa=self.empresa,
            horario="15:00"
        )

    def test_nao_permite_agendamento_duplicado(self):
        url = "/api/agendamentos/"
        payload = {
            "empresa": self.empresa.id,
            "nome": "Cliente 1",
            "telefone": "(62) 91111-1111",
            "data": "2026-04-15",
            "horario": self.horario.id,
            "observacoes": ""
        }

        response1 = self.client.post(url, payload, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(url, payload, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


class AgendamentoSegurancaTests(APITestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(
            nome="Empresa Segura",
            telefone="(62) 98888-0000"
        )

        self.horario = Horario.objects.create(
            empresa=self.empresa,
            horario="16:00"
        )

    def test_nao_permite_acesso_sem_token(self):
        url = "/api/agendamentos/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_nao_permite_criar_sem_token(self):
        url = "/api/agendamentos/"
        payload = {
            "empresa": self.empresa.id,
            "nome": "Sem Token",
            "telefone": "(62) 97777-0000",
            "data": "2026-04-20",
            "horario": self.horario.id,
            "observacoes": ""
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)