"""Models do módulo de auditorias: Unidade, Auditoria, ItemChecklist, RespostaItem."""
from django.conf import settings
from django.db import models
from django.utils import timezone


class Unidade(models.Model):
    """Filial/unidade auditada."""

    nome = models.CharField(max_length=200, verbose_name='Nome')
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    ativa = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'
        ordering = ['nome']

    def __str__(self):
        return f'{self.codigo} — {self.nome}'


class Auditoria(models.Model):
    """Registro de uma auditoria de fiscalização periódica."""

    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('finalizada', 'Finalizada'),
    ]

    documento = models.CharField(max_length=20, unique=True, editable=False, verbose_name='Documento')
    unidade = models.ForeignKey(
        Unidade,
        on_delete=models.PROTECT,
        related_name='auditorias',
        verbose_name='Unidade',
    )
    data = models.DateField(verbose_name='Data da Auditoria')
    fiscal = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='auditorias_como_fiscal',
        verbose_name='Fiscal PFIS',
    )
    responsavel_tecnico = models.CharField(max_length=200, verbose_name='Responsável Técnico')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='rascunho', verbose_name='Status')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Auditoria'
        verbose_name_plural = 'Auditorias'
        ordering = ['-criado_em']

    def __str__(self):
        return self.documento

    def save(self, *args, **kwargs):
        if not self.documento:
            self.documento = self._gerar_documento()
        super().save(*args, **kwargs)

    def _gerar_documento(self):
        """Gera ID no formato PFIS-YYYY-NNNN, seguro contra race conditions."""
        from django.db import transaction
        ano = timezone.now().year
        with transaction.atomic():
            count = Auditoria.objects.select_for_update().filter(
                documento__startswith=f'PFIS-{ano}-'
            ).count()
        return f'PFIS-{ano}-{str(count + 1).zfill(4)}'

    @property
    def total_itens(self):
        return self.respostas.count()

    @property
    def conformes(self):
        return self.respostas.filter(status='conforme').count()

    @property
    def nao_conformes(self):
        return self.respostas.filter(status='nao_conforme').count()

    @property
    def nao_aplicaveis(self):
        return self.respostas.filter(status='nao_aplicavel').count()

    @property
    def pendentes(self):
        return self.respostas.filter(status='pendente').count()

    @property
    def indice_conformidade(self):
        if self.total_itens == 0:
            return 0.0
        return round((self.conformes / self.total_itens) * 100, 1)

    @property
    def progresso(self):
        if self.total_itens == 0:
            return 0
        return round(((self.total_itens - self.pendentes) / self.total_itens) * 100)

    def pode_finalizar(self):
        return self.pendentes == 0 and self.total_itens > 0


class ItemChecklist(models.Model):
    """Item do checklist de fiscalização — cadastro fixo de 119 itens."""

    PERIODICIDADE_CHOICES = [
        ('diario', 'Diário'),
        ('semanal', 'Semanal'),
        ('mensal', 'Mensal'),
        ('semestral', 'Semestral'),
        ('anual', 'Anual'),
    ]

    numero = models.IntegerField(unique=True, verbose_name='Número')
    secao = models.CharField(max_length=150, verbose_name='Seção')
    periodicidade = models.CharField(max_length=15, choices=PERIODICIDADE_CHOICES, verbose_name='Periodicidade')
    texto = models.TextField(verbose_name='Texto do Item')
    apontamento = models.TextField(blank=True, verbose_name='Apontamento/Instrução')

    class Meta:
        verbose_name = 'Item do Checklist'
        verbose_name_plural = 'Itens do Checklist'
        ordering = ['numero']

    def __str__(self):
        return f'{self.numero}. {self.texto[:60]}'


class RespostaItem(models.Model):
    """Resposta de um item de checklist em uma auditoria específica."""

    STATUS_CHOICES = [
        ('conforme', 'Conforme'),
        ('nao_conforme', 'Não Conforme'),
        ('nao_aplicavel', 'Não Aplicável'),
        ('pendente', 'Pendente'),
    ]

    auditoria = models.ForeignKey(
        Auditoria,
        on_delete=models.CASCADE,
        related_name='respostas',
        verbose_name='Auditoria',
    )
    item = models.ForeignKey(
        ItemChecklist,
        on_delete=models.PROTECT,
        related_name='respostas',
        verbose_name='Item',
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pendente', verbose_name='Status')
    observacao = models.TextField(blank=True, verbose_name='Observação')
    evidencia_bytes = models.BinaryField(blank=True, null=True, editable=False, verbose_name='Evidência (bytes)')
    evidencia_content_type = models.CharField(max_length=100, blank=True, verbose_name='MIME type')
    evidencia_filename = models.CharField(max_length=255, blank=True, verbose_name='Nome do arquivo')
    respondido_em = models.DateTimeField(auto_now=True)

    @property
    def tem_evidencia(self):
        return bool(self.evidencia_bytes)

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        unique_together = [['auditoria', 'item']]
        ordering = ['item__numero']

    def __str__(self):
        return f'{self.auditoria.documento} — Item {self.item.numero}'
