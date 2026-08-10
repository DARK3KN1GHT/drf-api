from django.core.management.base import BaseCommand

from agenda.models import Empresa, Horario


class Command(BaseCommand):
    help = "Cria e atualiza empresas e horários iniciais sem duplicar registros."

    def handle(self, *args, **options):

        empresas = [
            {
                "nome": "EMPRESA A",
                "telefone": "(62) 90000-0000",
                "horarios": [
                    "07:00",
                    "08:00",
                    "09:00",
                    "10:00",
                    "11:00",
                    "13:00",
                    "14:00",
                    "15:00",
                    "16:00",
                    "17:00",
                    "18:00",
                    "19:00",
                ],
            },
            {
                "nome": "EMPRESA B",
                "telefone": "(62) 90000-0000",
                "horarios": [
                    "07:00",
                    "08:00",
                    "09:00",
                    "10:00",
                    "11:00",
                    "13:00",
                    "14:00",
                    "15:00",
                    "16:00",
                    "17:00",
                ],
            },
        ]

        for dados in empresas:

            # Cria a empresa se não existir.
            # Se já existir, atualiza o telefone.
            empresa, criada = Empresa.objects.update_or_create(
                nome=dados["nome"],
                defaults={
                    "telefone": dados["telefone"],
                },
            )

            if criada:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Empresa criada: {empresa.nome}"
                    )
                )
            else:
                self.stdout.write(
                    f"Empresa atualizada: {empresa.nome}"
                )

            # Cria os horários permitidos para cada empresa
            for horario in dados["horarios"]:
                _, horario_criado = Horario.objects.get_or_create(
                    empresa=empresa,
                    horario=horario,
                )

                if horario_criado:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Horário criado: {empresa.nome} - {horario}"
                        )
                    )

        # =====================================================
        # EMPRESA B funciona somente até 17:00
        # =====================================================

        empresa_b = Empresa.objects.filter(
            nome="EMPRESA B"
        ).first()

        if empresa_b:
            removidos, _ = Horario.objects.filter(
                empresa=empresa_b,
                horario__gt="17:00",
            ).delete()

            if removidos:
                self.stdout.write(
                    self.style.WARNING(
                        f"{removidos} horário(s) após 17:00 "
                        "removido(s) da EMPRESA B."
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Dados iniciais configurados com sucesso."
            )
        )