from django.urls import path
from . import views

urlpatterns = [
    path('auditorias/<int:pk>/pdf/', views.AuditoriaPDFView.as_view(), name='auditoria_pdf'),
]
