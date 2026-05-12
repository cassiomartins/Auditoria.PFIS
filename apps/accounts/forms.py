from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser


class LoginForm(AuthenticationForm):
    """Formulário de login com estilo customizado."""

    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-transparent border-b border-outline-variant focus:border-primary p-2 text-lg focus:ring-0 focus:outline-none transition-colors',
            'placeholder': 'seu.usuario',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-transparent border-b border-outline-variant focus:border-primary p-2 text-lg focus:ring-0 focus:outline-none transition-colors',
            'placeholder': '••••••••',
        }),
    )


class UsuarioForm(forms.ModelForm):
    """Formulário para criação/edição de usuários pelo Gestor."""

    password = forms.CharField(
        label='Senha',
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-surface-container-low rounded p-2 border-0 focus:ring-1 focus:ring-primary',
            'placeholder': 'Deixe em branco para manter a senha atual',
        }),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'perfil', 'unidade', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full bg-surface-container-low rounded p-2 border-0 focus:ring-1 focus:ring-primary'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full bg-surface-container-low rounded p-2 border-0 focus:ring-1 focus:ring-primary'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full bg-surface-container-low rounded p-2 border-0 focus:ring-1 focus:ring-primary'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-surface-container-low rounded p-2 border-0 focus:ring-1 focus:ring-primary'}),
            'perfil': forms.Select(attrs={'class': 'w-full bg-surface-container-low rounded p-2 border-0 focus:ring-1 focus:ring-primary'}),
            'unidade': forms.Select(attrs={'class': 'w-full bg-surface-container-low rounded p-2 border-0 focus:ring-1 focus:ring-primary'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
