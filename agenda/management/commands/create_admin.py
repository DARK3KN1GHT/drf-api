import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Cria ou atualiza um superusuário usando variáveis de ambiente."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_ADMIN_USERNAME")
        email = os.environ.get("DJANGO_ADMIN_EMAIL")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.ERROR(
                    "DJANGO_ADMIN_USERNAME e DJANGO_ADMIN_PASSWORD são obrigatórios."
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email or "",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.is_staff = True
        user.is_superuser = True

        if email:
            user.email = email

        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS("Superusuário criado com sucesso.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Superusuário atualizado com sucesso.")
            )