from django.urls import path
from .views import ValidarSmartContract
from .views import ValidarBeneficiario
urlpatterns = [
    path('validar-smart-contract/', ValidarSmartContract.as_view(), name='validar_smart_contract'),
    path("validar-beneficiario/", ValidarBeneficiario.as_view(), name='validar_beneficiario')
] 
