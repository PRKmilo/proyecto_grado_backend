from django.urls import path
from .views  import NotificacionCreateView, NotificacionListUser

urlpatterns = [
    path('escrituras/<str:escritura_id>/', NotificacionListUser.as_view(), name='notificaciones-escritura'),
    path()

]


