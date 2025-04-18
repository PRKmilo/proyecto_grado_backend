# notificaciones/urls.py

from django.urls import path
from .views import CorreccionView

urlpatterns = [
    path('correcciones/usuario/<str:user_id>/', CorreccionView.as_view()),
]
