from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminForDeleteOtherwiseAuthenticatedOrReadOnly(BasePermission):
    """
    Regras:
    - leitura (GET, HEAD, OPTIONS): qualquer pessoa
    - POST, PUT, PATCH: usuário autenticado
    - DELETE: apenas staff/admin
    """

    def has_permission(self, request, view):
        # leitura liberada para qualquer pessoa
        if request.method in SAFE_METHODS:
            return True

        # delete só staff/admin
        if request.method == "DELETE":
            return bool(request.user and request.user.is_authenticated and request.user.is_staff)

        # create/update para usuário autenticado
        return bool(request.user and request.user.is_authenticated)