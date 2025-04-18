from django.urls import path
from .views import EscrituraListCreateView, EscrituraUpdateView, EscrituraConsultaEtapa, EscrituraActualizacionPdf

urlpatterns = [
    path('escrituras/', EscrituraListCreateView.as_view(), name='escrituras-list-create'),  # GET y POST
    path('escrituras/<str:escritura_id>/', EscrituraUpdateView.as_view(), name='escrituras-update'),
    path('escrituras/pdf_actualizacion/<str:escritura_id>/', EscrituraActualizacionPdf.as_view(), name='escritura-pdf'), 
    path('consultar-etapa/<str:escritura_id>/', EscrituraConsultaEtapa.as_view(), name='escrituras-etapa'),
]
