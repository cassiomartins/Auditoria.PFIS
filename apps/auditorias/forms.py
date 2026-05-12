from django import forms
from .models import Auditoria, RespostaItem, Unidade


class AuditoriaForm(forms.ModelForm):
    """Formulário de criação de nova auditoria."""

    class Meta:
        model = Auditoria
        fields = ('unidade', 'data', 'responsavel_tecnico')
        widgets = {
            'unidade': forms.Select(attrs={
                'class': 'w-full bg-transparent border-b border-outline-variant focus:border-primary p-2 focus:ring-0 focus:outline-none transition-colors',
            }),
            'data': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full bg-transparent border-b border-outline-variant focus:border-primary p-2 focus:ring-0 focus:outline-none transition-colors',
            }),
            'responsavel_tecnico': forms.TextInput(attrs={
                'class': 'w-full bg-transparent border-b border-outline-variant focus:border-primary p-2 focus:ring-0 focus:outline-none transition-colors',
                'placeholder': 'Nome do Responsável Técnico',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unidade'].queryset = Unidade.objects.filter(ativa=True)
        self.fields['unidade'].empty_label = 'Selecione a unidade...'


class RespostaItemForm(forms.ModelForm):
    """Formulário de resposta de um item — usado via HTMX."""

    class Meta:
        model = RespostaItem
        fields = ('status', 'observacao')
        widgets = {
            'status': forms.HiddenInput(),
            'observacao': forms.Textarea(attrs={
                'class': 'w-full bg-surface-container-low rounded-md text-sm p-3 border-0 focus:ring-1 focus:ring-primary resize-none',
                'placeholder': 'Descreva a observação ou desvio encontrado...',
                'rows': 3,
            }),
        }


