from django.urls import path
from .views import EscrituraListCreateView, EscrituraUpdateView

urlpatterns = [
    path('escrituras/', EscrituraListCreateView.as_view(), name='escrituras-list-create'),  # GET y POST
    path('escrituras/<int:escritura_id>/', EscrituraUpdateView.as_view(), name='escrituras-update'),  # GET y PUT
]
