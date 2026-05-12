from django.contrib import admin
from .models import Unidade, Auditoria, ItemChecklist, RespostaItem


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'ativa')
    list_filter = ('ativa',)
    search_fields = ('codigo', 'nome')


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('documento', 'unidade', 'data', 'fiscal', 'status', 'criado_em')
    list_filter = ('status', 'unidade')
    search_fields = ('documento', 'responsavel_tecnico')
    date_hierarchy = 'data'
    readonly_fields = ('documento', 'criado_em', 'atualizado_em')


@admin.register(ItemChecklist)
class ItemChecklistAdmin(admin.ModelAdmin):
    list_display = ('numero', 'secao', 'periodicidade', 'texto')
    list_filter = ('periodicidade', 'secao')
    search_fields = ('numero', 'texto')


@admin.register(RespostaItem)
class RespostaItemAdmin(admin.ModelAdmin):
    list_display = ('auditoria', 'item', 'status', 'respondido_em')
    list_filter = ('status',)
    search_fields = ('auditoria__documento',)
    raw_id_fields = ('auditoria', 'item')
