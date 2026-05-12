"""Modelo de usuário customizado com perfis de acesso."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Usuário do sistema com perfil de acesso diferenciado."""

    PERFIL_CHOICES = [
        ('gestor', 'Gestor'),
        ('fiscal', 'Fiscal PFIS'),
        ('responsavel_tecnico', 'Responsável Técnico'),
    ]

    perfil = models.CharField(
        max_length=20,
        choices=PERFIL_CHOICES,
        default='fiscal',
        verbose_name='Perfil',
    )
    unidade = models.ForeignKey(
        'auditorias.Unidade',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
        verbose_name='Unidade',
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_gestor(self):
        return self.perfil == 'gestor'

    @property
    def is_fiscal(self):
        return self.perfil == 'fiscal'

    @property
    def is_responsavel(self):
        return self.perfil == 'responsavel_tecnico'

    def get_perfil_display_badge(self):
        badges = {
            'gestor': 'bg-primary/10 text-primary',
            'fiscal': 'bg-secondary/10 text-secondary',
            'responsavel_tecnico': 'bg-tertiary/10 text-tertiary',
        }
        return badges.get(self.perfil, '')
