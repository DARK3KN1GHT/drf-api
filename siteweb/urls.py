from django.urls import path
from .views import home, agendar, sucesso

urlpatterns = [
    path('', home, name='home'),
    path('agendar/', agendar, name='agendar'),
    path('sucesso/', sucesso, name='sucesso'),
]