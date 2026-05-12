from django.urls import path
from . import views

urlpatterns = [
    path('auditorias/', views.AuditoriaListView.as_view(), name='auditorias'),
    path('auditorias/nova/', views.AuditoriaNovaView.as_view(), name='auditoria_nova'),
    path('auditorias/<int:pk>/', views.AuditoriaDetalheView.as_view(), name='auditoria_detalhe'),
    path('auditorias/<int:pk>/preencher/', views.AuditoriaPreencherView.as_view(), name='auditoria_preencher'),
    path('auditorias/<int:pk>/finalizar/', views.AuditoriaFinalizarView.as_view(), name='auditoria_finalizar'),
    path('auditorias/<int:pk>/responder/<int:resposta_id>/', views.ResponderItemView.as_view(), name='responder_item'),
    path('auditorias/<int:pk>/item/<int:resposta_id>/evidencia/', views.EvidenciaUploadView.as_view(), name='evidencia_upload'),
    path('auditorias/<int:pk>/item/<int:resposta_id>/evidencia/download/', views.EvidenciaDownloadView.as_view(), name='evidencia_download'),
]
