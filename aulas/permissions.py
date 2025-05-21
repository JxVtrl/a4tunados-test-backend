from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsProfessorOrReadOnly(BasePermission):
    """
    Permite apenas professores criarem, editarem ou deletarem vídeos.
    Alunos só podem visualizar (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and getattr(request.user, 'tipo', None) == 'professor'