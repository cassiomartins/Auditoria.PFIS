"""Mixins e utilitários compartilhados entre apps."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class GestorRequiredMixin(LoginRequiredMixin):
    """Restringe acesso a usuários com perfil Gestor."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.perfil != 'gestor':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class FiscalOuGestorMixin(LoginRequiredMixin):
    """Restringe acesso a Fiscal PFIS ou Gestor."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.perfil not in ('fiscal', 'gestor'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
