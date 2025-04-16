from django.urls import path
from .views import ProcesoListCreateView, ProcesoUpdateView, ProcesoEscritura

urlpatterns = [
    path('procesos/', ProcesoListCreateView.as_view(), name='procesos-list-create'),  # GET y POST
    path('procesos/<int:proceso_id>/', ProcesoUpdateView.as_view(), name='procesos-update'),  # GET y PUT
    path('procesos/escrituras/<int:proceso_id>', ProcesoEscritura.as_view() , name='proceso-escritura')
]
