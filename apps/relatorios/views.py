"""Geração de PDF com xhtml2pdf."""
import base64
import io
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View

from apps.auditorias.models import Auditoria, RespostaItem


class AuditoriaPDFView(LoginRequiredMixin, View):
    """Gera o PDF do relatório de auditoria via xhtml2pdf."""

    def get(self, request, pk):
        auditoria = get_object_or_404(Auditoria, pk=pk)

        respostas = (
            RespostaItem.objects
            .select_related('item')
            .filter(auditoria=auditoria)
            .order_by('item__numero')
        )

        for r in respostas:
            if r.evidencia_bytes:
                ct = r.evidencia_content_type or 'image/jpeg'
                b64 = base64.b64encode(bytes(r.evidencia_bytes)).decode('ascii')
                r.evidencia_data_url = f'data:{ct};base64,{b64}'
            else:
                r.evidencia_data_url = None

        secoes = {}
        for r in respostas:
            s = r.item.secao
            if s not in secoes:
                secoes[s] = []
            secoes[s].append(r)

        html_string = render_to_string('relatorios/pdf.html', {
            'auditoria': auditoria,
            'secoes': secoes,
            'gerado_em': timezone.now(),
            'gerado_por': request.user,
        })

        from xhtml2pdf import pisa
        pdf_file = io.BytesIO()
        pisa.CreatePDF(html_string, dest=pdf_file, encoding='utf-8')
        pdf_file.seek(0)

        filename = f'{auditoria.documento}.pdf'
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response
