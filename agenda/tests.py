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

    def test_nao_permite_mais_de_dois_agendamentos_no_mesmo_horario(self):
        url = "/api/agendamentos/"

        payload1 = {
            "empresa": self.empresa.id,
            "nome": "Cliente 1",
            "telefone": "(62) 91111-1111",
            "data": "2026-04-15",
            "horario": self.horario.id,
            "observacoes": ""
        }

        payload2 = {
            "empresa": self.empresa.id,
            "nome": "Cliente 2",
            "telefone": "(62) 92222-2222",
            "data": "2026-04-15",
            "horario": self.horario.id,
            "observacoes": ""
        }

        payload3 = {
            "empresa": self.empresa.id,
            "nome": "Cliente 3",
            "telefone": "(62) 93333-3333",
            "data": "2026-04-15",
            "horario": self.horario.id,
            "observacoes": ""
        }

        response1 = self.client.post(url, payload1, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post(url, payload2, format="json")
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        response3 = self.client.post(url, payload3, format="json")
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)


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

    def test_permite_leitura_sem_token(self):
        url = "/api/agendamentos/"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

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

class AgendamentoUpdateAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teste_update",
            password="123456"
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        self.empresa = Empresa.objects.create(
            nome="Empresa Update",
            telefone="(62) 98888-1234"
        )

        self.horario = Horario.objects.create(
            empresa=self.empresa,
            horario="16:00"
        )

        self.agendamento = Agendamento.objects.create(
            empresa=self.empresa,
            horario=self.horario,
            data=date(2026, 9, 10),
            nome="Cliente Teste",
            telefone="(62) 91111-1111",
            observacoes=""
        )

    def test_edita_telefone_com_patch(self):
        url = f"/api/agendamentos/{self.agendamento.id}/"

        payload = {
            "telefone": "(62) 99999-9999"
        }

        response = self.client.patch(
            url,
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.agendamento.refresh_from_db()

        self.assertEqual(
            self.agendamento.telefone,
            "(62) 99999-9999"
        )

        self.assertEqual(
            self.agendamento.nome,
            "Cliente Teste"
        )

    def test_edita_agendamento_com_put(self):
        url = f"/api/agendamentos/{self.agendamento.id}/"

        payload = {
            "empresa": self.empresa.id,
            "nome": "Cliente Atualizado",
            "telefone": "(62) 98888-8888",
            "data": "2026-09-11",
            "horario": self.horario.id,
            "observacoes": "Atualizado via PUT"
        }

        response = self.client.put(
            url,
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.agendamento.refresh_from_db()

        self.assertEqual(
            self.agendamento.nome,
            "Cliente Atualizado"
        )

        self.assertEqual(
            self.agendamento.telefone,
            "(62) 98888-8888"
        )

        self.assertEqual(
            str(self.agendamento.data),
            "2026-09-11"
        )

        self.assertEqual(
            self.agendamento.observacoes,
            "Atualizado via PUT"
        )

    def test_usuario_comum_nao_pode_excluir_agendamento(self):
        url = f"/api/agendamentos/{self.agendamento.id}/"

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertTrue(
            Agendamento.objects.filter(
                id=self.agendamento.id
            ).exists()
        )

    def test_admin_pode_excluir_agendamento(self):
        admin = User.objects.create_user(
            username="admin_delete",
            password="123456",
            is_staff=True
        )

        refresh = RefreshToken.for_user(admin)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        url = f"/api/agendamentos/{self.agendamento.id}/"

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Agendamento.objects.filter(
                id=self.agendamento.id
            ).exists()
        )

class AgendamentoFiltroAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teste_filtro",
            password="123456"
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        self.empresa1 = Empresa.objects.create(
            nome="Empresa 1",
            telefone="(62) 90000-0001"
        )

        self.empresa2 = Empresa.objects.create(
            nome="Empresa 2",
            telefone="(62) 90000-0002"
        )

        self.horario1 = Horario.objects.create(
            empresa=self.empresa1,
            horario="08:00"
        )

        self.horario2 = Horario.objects.create(
            empresa=self.empresa2,
            horario="09:00"
        )

        Agendamento.objects.create(
            empresa=self.empresa1,
            horario=self.horario1,
            data=date(2026, 9, 15),
            nome="Cliente Empresa 1",
            telefone="(62) 91111-1111",
            observacoes=""
        )

        Agendamento.objects.create(
            empresa=self.empresa2,
            horario=self.horario2,
            data=date(2026, 9, 15),
            nome="Cliente Empresa 2",
            telefone="(62) 92222-2222",
            observacoes=""
        )

    def test_ordena_agendamentos_por_nome(self):
        url = "/api/agendamentos/?ordering=nome"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        nomes = [
            item["nome"]
            for item in response.data["results"]
        ]

        self.assertEqual(
            nomes,
            sorted(nomes)
        )

    def test_paginacao_agendamentos(self):
        for i in range(6):
            Agendamento.objects.create(
                empresa=self.empresa1,
                horario=self.horario1,
                data=date(2026, 9, 20 + i),
                nome=f"Cliente Extra {i}",
                telefone=f"(62) 93333-33{i:02d}",
                observacoes=""
            )

        url = "/api/agendamentos/"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data["results"]),
            5
        )

        self.assertIsNotNone(
            response.data["next"]
        )

    def test_filtra_agendamentos_por_empresa(self):
            url = f"/api/agendamentos/?empresa={self.empresa1.id}"

            response = self.client.get(url)

            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )

            self.assertEqual(
                response.data["count"],
                1
            )

            self.assertEqual(
                response.data["results"][0]["nome"],
                "Cliente Empresa 1"
            )

    def test_filtra_agendamentos_por_data(self):
        url = "/api/agendamentos/?data=2026-09-15"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            2
        )

        nomes = [
            item["nome"]
            for item in response.data["results"]
        ]

        self.assertIn(
            "Cliente Empresa 1",
            nomes
        )

        self.assertIn(
            "Cliente Empresa 2",
            nomes
        )

    def test_busca_agendamentos_por_nome(self):
        url = "/api/agendamentos/?search=Cliente Empresa 1"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

        self.assertEqual(
            response.data["results"][0]["nome"],
            "Cliente Empresa 1"
        )

class JWTAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teste_jwt",
            password="123456"
        )

        self.empresa = Empresa.objects.create(
            nome="Empresa JWT",
            telefone="(62) 99999-0000"
        )

        self.horario = Horario.objects.create(
            empresa=self.empresa,
            horario="11:00"
        )

        Agendamento.objects.create(
            empresa=self.empresa,
            horario=self.horario,
            data=date(2026, 9, 20),
            nome="Cliente JWT",
            telefone="(62) 98888-0000",
            observacoes=""
        )

    def test_obtem_token_jwt(self):
        url = "/api/token/"

        payload = {
            "username": "teste_jwt",
            "password": "123456"
        }

        response = self.client.post(
            url,
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_renova_access_token(self):
        refresh = RefreshToken.for_user(self.user)

        url = "/api/token/refresh/"

        payload = {
            "refresh": str(refresh)
        }

        response = self.client.post(
            url,
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("access", response.data)

    def test_acessa_agendamentos_com_token(self):
        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        url = "/api/agendamentos/"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
