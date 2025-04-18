from django.urls import path
from .views import ( 
UsuarioListCreateView, 
UsuarioUpdateView, 
UsuarioJuez, 
UsuarioNotario,
LoginView,
ActivarMFAView,
VerificarMFAView,
JWTProtectedView,
CuentaDesbloqueo,
RolValidacion
)

urlpatterns = [
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuarios-list-create'),  # GET y POST
    path('usuarios/<int:usuario_id>/', UsuarioUpdateView.as_view(), name='usuarios-update'), # GET y PUT
    path('usuarios/juez/', UsuarioJuez.as_view(), name='usuarios-juez'),
    path('usuarios/notario/', UsuarioNotario.as_view(), name='usuario-notario'),
    path("login/", LoginView.as_view(), name="login"),
    path("mfa/activar/", ActivarMFAView.as_view(), name="activar-mfa"),
    path("mfa/verificar/", VerificarMFAView.as_view(), name="verificar-mfa"),

    path("desbloquear-cuenta/<str:escritura_id>/", CuentaDesbloqueo.as_view(), name="cuenta-desbloqueo"),
    path("rol-validacion/<str:escritura_id>/", RolValidacion.as_view(), name="rol-validacion"),

    # 📌 Endpoint protegido con JWT
    path("protegido/<str:escritura_id>/", JWTProtectedView.as_view(), name="jwt-protected"),

]
