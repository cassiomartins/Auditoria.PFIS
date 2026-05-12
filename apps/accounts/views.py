"""Views de autenticação, dashboard e gerenciamento de usuários."""
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from apps.core.mixins import GestorRequiredMixin
from apps.auditorias.models import Auditoria
from .models import CustomUser
from .forms import LoginForm, UsuarioForm


class LoginView(View):
    """Tela de login."""

    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        from django.shortcuts import render
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request):
        from django.shortcuts import render
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')

    def get(self, request):
        logout(request)
        return redirect('login')


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal — conteúdo varia por perfil."""

    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_gestor:
            auditorias = Auditoria.objects.select_related('unidade', 'fiscal').all()
        elif user.is_fiscal:
            auditorias = Auditoria.objects.select_related('unidade', 'fiscal').filter(fiscal=user)
        else:
            auditorias = Auditoria.objects.select_related('unidade', 'fiscal').filter(
                unidade=user.unidade
            ) if user.unidade else Auditoria.objects.none()

        ctx['auditorias_recentes'] = auditorias.order_by('-criado_em')[:5]
        ctx['total'] = auditorias.count()
        ctx['rascunhos'] = auditorias.filter(status='rascunho').count()
        ctx['finalizadas'] = auditorias.filter(status='finalizada').count()
        return ctx


class UsuarioListView(GestorRequiredMixin, ListView):
    """Lista de usuários — apenas Gestor."""

    model = CustomUser
    template_name = 'accounts/usuarios.html'
    context_object_name = 'usuarios'
    queryset = CustomUser.objects.select_related('unidade').order_by('first_name', 'username')


class UsuarioCreateView(GestorRequiredMixin, CreateView):
    """Criação de novo usuário — apenas Gestor."""

    model = CustomUser
    form_class = UsuarioForm
    template_name = 'accounts/usuario_form.html'
    success_url = reverse_lazy('usuarios')

    def form_valid(self, form):
        messages.success(self.request, 'Usuário criado com sucesso.')
        return super().form_valid(form)


class UsuarioUpdateView(GestorRequiredMixin, UpdateView):
    """Edição de usuário — apenas Gestor."""

    model = CustomUser
    form_class = UsuarioForm
    template_name = 'accounts/usuario_form.html'
    success_url = reverse_lazy('usuarios')

    def form_valid(self, form):
        messages.success(self.request, 'Usuário atualizado com sucesso.')
        return super().form_valid(form)
