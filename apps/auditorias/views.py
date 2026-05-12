"""Views do módulo de auditorias com suporte a HTMX."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse

from apps.core.mixins import FiscalOuGestorMixin
from .models import Auditoria, ItemChecklist, RespostaItem, Unidade
from .forms import AuditoriaForm, RespostaItemForm


class AuditoriaListView(LoginRequiredMixin, ListView):
    """Lista de auditorias filtrada por perfil do usuário."""

    model = Auditoria
    template_name = 'auditorias/lista.html'
    context_object_name = 'auditorias'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        qs = Auditoria.objects.select_related('unidade', 'fiscal')
        if user.is_gestor:
            return qs
        if user.is_fiscal:
            return qs.filter(fiscal=user)
        if user.is_responsavel and user.unidade:
            return qs.filter(unidade=user.unidade)
        return Auditoria.objects.none()


class AuditoriaNovaView(FiscalOuGestorMixin, CreateView):
    """Criação de nova auditoria — instancia 119 RespostaItem automaticamente."""

    model = Auditoria
    form_class = AuditoriaForm
    template_name = 'auditorias/nova.html'

    def form_valid(self, form):
        auditoria = form.save(commit=False)
        auditoria.fiscal = self.request.user
        auditoria.save()

        itens = ItemChecklist.objects.all()
        RespostaItem.objects.bulk_create([
            RespostaItem(auditoria=auditoria, item=item, status='pendente')
            for item in itens
        ])

        messages.success(self.request, f'Auditoria {auditoria.documento} criada. Preencha os itens abaixo.')
        return redirect('auditoria_preencher', pk=auditoria.pk)


class AuditoriaPreencherView(LoginRequiredMixin, DetailView):
    """Tela de preenchimento da auditoria com accordions HTMX."""

    model = Auditoria
    template_name = 'auditorias/preencher.html'

    def get_object(self, queryset=None):
        auditoria = get_object_or_404(Auditoria, pk=self.kwargs['pk'])
        user = self.request.user
        if not (user.is_gestor or auditoria.fiscal == user):
            raise PermissionDenied
        if auditoria.status == 'finalizada':
            return redirect('auditoria_detalhe', pk=auditoria.pk)
        return auditoria

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        auditoria = self.object
        respostas = (
            RespostaItem.objects
            .select_related('item')
            .filter(auditoria=auditoria)
            .order_by('item__numero')
        )
        secoes = {}
        for r in respostas:
            s = r.item.secao
            if s not in secoes:
                secoes[s] = []
            secoes[s].append(r)
        ctx['secoes'] = secoes
        ctx['auditoria'] = auditoria
        return ctx


class AuditoriaDetalheView(LoginRequiredMixin, DetailView):
    """Visualização somente-leitura da auditoria."""

    model = Auditoria
    template_name = 'auditorias/detalhe.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        auditoria = self.object
        respostas = (
            RespostaItem.objects
            .select_related('item')
            .filter(auditoria=auditoria)
            .order_by('item__numero')
        )
        secoes = {}
        for r in respostas:
            s = r.item.secao
            if s not in secoes:
                secoes[s] = []
            secoes[s].append(r)
        ctx['secoes'] = secoes
        return ctx


class AuditoriaFinalizarView(LoginRequiredMixin, View):
    """Grava e finaliza a auditoria."""

    def post(self, request, pk):
        auditoria = get_object_or_404(Auditoria, pk=pk)
        if auditoria.fiscal != request.user and not request.user.is_gestor:
            raise PermissionDenied
        auditoria.status = 'finalizada'
        auditoria.save(update_fields=['status'])
        messages.success(request, f'Auditoria {auditoria.documento} gravada com sucesso.')
        return redirect('auditoria_detalhe', pk=pk)


class ResponderItemView(LoginRequiredMixin, View):
    """Salva a resposta de um item via HTMX — retorna partial HTML."""

    def post(self, request, pk, resposta_id):
        auditoria = get_object_or_404(Auditoria, pk=pk)
        resposta = get_object_or_404(RespostaItem, pk=resposta_id, auditoria=auditoria)

        if auditoria.status == 'finalizada':
            return HttpResponse(status=403)
        if auditoria.fiscal != request.user and not request.user.is_gestor:
            return HttpResponse(status=403)

        novo_status = request.POST.get('status', 'pendente')
        observacao = request.POST.get('observacao', '').strip()

        if novo_status not in ('conforme', 'nao_conforme', 'nao_aplicavel', 'pendente'):
            return HttpResponse(status=400)

        if novo_status == 'nao_conforme' and not observacao:
            observacao = ''

        resposta.status = novo_status
        resposta.observacao = observacao
        resposta.save(update_fields=['status', 'observacao', 'respondido_em'])

        auditoria.refresh_from_db()

        return render(request, 'auditorias/partials/item_resposta.html', {
            'resposta': resposta,
            'auditoria': auditoria,
            'oob_progress': True,
        })


class EvidenciaUploadView(LoginRequiredMixin, View):
    """Upload de evidência fotográfica via HTMX — armazenada como BLOB no banco."""

    def post(self, request, pk, resposta_id):
        auditoria = get_object_or_404(Auditoria, pk=pk)
        resposta = get_object_or_404(RespostaItem, pk=resposta_id, auditoria=auditoria)

        if auditoria.status == 'finalizada':
            return HttpResponse(status=403)
        if auditoria.fiscal != request.user and not request.user.is_gestor:
            return HttpResponse(status=403)

        arquivo = request.FILES.get('evidencia')
        if arquivo:
            resposta.evidencia_bytes = arquivo.read()
            resposta.evidencia_content_type = arquivo.content_type or 'image/jpeg'
            resposta.evidencia_filename = arquivo.name
            resposta.save(update_fields=['evidencia_bytes', 'evidencia_content_type', 'evidencia_filename'])

        return render(request, 'auditorias/partials/evidencia_upload.html', {
            'resposta': resposta,
            'auditoria': auditoria,
        })


class EvidenciaDownloadView(LoginRequiredMixin, View):
    """Serve a evidência fotográfica armazenada como BLOB no banco."""

    def get(self, request, pk, resposta_id):
        resposta = get_object_or_404(RespostaItem, pk=resposta_id, auditoria__pk=pk)
        if not resposta.evidencia_bytes:
            return HttpResponse(status=404)
        content_type = resposta.evidencia_content_type or 'image/jpeg'
        response = HttpResponse(bytes(resposta.evidencia_bytes), content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{resposta.evidencia_filename}"'
        return response
