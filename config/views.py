from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(["GET"])
def api_root(request):
    return Response({
        "name": "Agenda API",
        "status": "online",
        "version": "v1",
        "docs": {
            "swagger": request.build_absolute_uri("/api/docs/"),
            "redoc": request.build_absolute_uri("/api/redoc/"),
        },
        "endpoints": {
            "agendamentos": reverse("agendamentos-list", request=request),
            "admin": request.build_absolute_uri("/admin/"),
        }
    })