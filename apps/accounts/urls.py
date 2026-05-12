from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('usuarios/', views.UsuarioListView.as_view(), name='usuarios'),
    path('usuarios/novo/', views.UsuarioCreateView.as_view(), name='usuario_novo'),
    path('usuarios/<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario_editar'),
    path('', lambda request: __import__('django.shortcuts', fromlist=['redirect']).redirect('dashboard'), name='home'),
]
