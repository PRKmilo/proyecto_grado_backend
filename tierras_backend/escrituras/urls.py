from django.urls import path
from .views import EscrituraListCreateView, EscrituraUpdateView, EscrituraConsultaEtapa

urlpatterns = [
    path('escrituras/', EscrituraListCreateView.as_view(), name='escrituras-list-create'),  # GET y POST
    path('escrituras/<int:escritura_id>/', EscrituraUpdateView.as_view(), name='escrituras-update'),
    
    path('consultar-etapa/<str:escritura_id>/', EscrituraConsultaEtapa.as_view(), name='escrituras-etapa'),
]
