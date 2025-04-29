from django.urls import path
from .views import ProcesoListCreateView, ProcesoUpdateView, ProcesoEscritura, ProcesoBeneficiario

urlpatterns = [
    path('procesos/', ProcesoListCreateView.as_view(), name='procesos-list-create'),  # GET y POST
    path('procesos/<int:proceso_id>/', ProcesoUpdateView.as_view(), name='procesos-update'),  # GET y PUT
    path('procesos/usuario/<str:user_id>/', ProcesoBeneficiario.as_view() , name='proceso-beneficiario'),
    path('procesos/escrituras/<int:proceso_id>', ProcesoEscritura.as_view() , name='proceso-escritura')
]
