import pyotp
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Usuario, MFADevice
from .serializers import UsuarioSerializer, MFASerializer
from .models import UsuarioRol
from .authentication import AuthenticationService
from rest_framework_simplejwt.tokens import RefreshToken
from escrituras.networkService.smart_contract import SmartContract
from escrituras.networkService.credentials import Credentials
from escrituras.models.escritura import Escritura
# Create your views here.

class UsuarioListCreateView(APIView):
    
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)

        if serializer.is_valid():
            usuario = serializer.save()

            # Hash de la contraseña si se proporciona
            password_plaintext = request.data.get("hash_password")
            if password_plaintext:
                hashed_password = bcrypt.hashpw(password_plaintext.encode(), bcrypt.gensalt()).decode()
                usuario.hash_password = hashed_password
                usuario.save()

            # Retornar datos SIN la contraseña hasheada
            response_data = serializer.data
            response_data.pop("hash_password", None)  # 🔐 Elimina la contraseña antes de enviarla

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioUpdateView(APIView):
    """
    GET: Obtener un proceso por ID
    PUT: Actualizar un proceso existente
    """
    def get(self, request, usuario_id):
        permission_classes = [IsAuthenticated]
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, usuario_id):
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
        except Proceso.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuarioJuez(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        usuarios_jueces = Usuario.objects.filter(
            cedula__in=UsuarioRol.objects.filter(rol_id=7).values_list('usuario_id', flat=True)
        ).values()
        return Response(list(usuarios_jueces))

class UsuarioNotario(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        usuarios_notarios = Usuario.objects.filter(
          cedula__in=UsuarioRol.objects.filter(rol_id=6).values_list('usuario_id', flat=True)
        ).values()
        return Response(list(usuarios_notarios))
 


class LoginView(APIView):
    def post(self, request):
        cedula = request.data.get("cedula")
        password = request.data.get("password")

        if not cedula or not password:
            return Response({"error": "Cédula y contraseña requeridas"}, status=status.HTTP_400_BAD_REQUEST)

        user = AuthenticationService.autenticar_usuario(cedula, password)
        print("---------------user 1-------------------------")
        print(user)
        print("-----------------------------------------------")
        if user is None:
            return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)

        if MFADevice.objects.filter(user=user, is_active=True).exists():
            return Response({"mfa_required": True}, status=status.HTTP_200_OK)
        
        usuario_rol = UsuarioRol.objects.filter(usuario_id=user.cedula).values_list('rol_id', flat=True).first()

        print(usuario_rol)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'usuario_rol': str(usuario_rol)
        }) 
        


class ActivarMFAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        secret = pyotp.random_base32()
        print("ingresa en post ------------------------------")
    
        mfa_device, created = MFADevice.objects.update_or_create(
            user=request.user, defaults={"secret": secret, "is_active": True}
        )

        qr_uri = mfa_device.generate_totp_uri()
        return Response({"qr_uri": qr_uri}, status=status.HTTP_200_OK)

"""
class VerificarMFAView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        codigo = request.data.get("codigo")
        print("este es el codigo")
        print(codigo)
        print("este es el usuario")
        print(request.user)
        if not codigo:
            return Response({"error": "Código MFA requerido"}, status=status.HTTP_400_BAD_REQUEST)
        print("linea antes de 404 ")
        mfa_device = get_object_or_404(MFADevice, user=request.user, is_active=True)
        print("linea desues de 404")
        if not mfa_device.verify_code(codigo):


            return Response({"error": "Código MFA incorrecto"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(request.user)
        access_token = str(refresh.access_token)

        return Response({
            "refresh": str(refresh),
            "access": access_token
        }, status=status.HTTP_200_OK)       

        #token = AuthenticationService.generar_jwt(request.user)
        #return Response({"token": token}, status=status.HTTP_200_OK)
"""
class VerificarMFAView(APIView):
    def post(self, request):
        codigo = request.data.get("codigo")
        email = request.data.get("email")  # 🔹 Agregar email en el request

        print("Código recibido:", codigo)
        print("Email recibido:", email)

        if not codigo or not email:
            return Response({"error": "Código MFA y email requeridos"}, status=status.HTTP_400_BAD_REQUEST)

        # 🔹 Buscar usuario por email
        user = get_object_or_404(Usuario, email=email)
        print("Usuario encontrado:", user)

        # 🔹 Buscar el dispositivo MFA activo del usuario
        mfa_device = get_object_or_404(MFADevice, user=user, is_active=True)

        if not mfa_device.verify_code(codigo):
            return Response({"error": "Código MFA incorrecto"}, status=status.HTTP_400_BAD_REQUEST)

        # 🔹 Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "refresh": str(refresh),
            "access": access_token
        }, status=status.HTTP_200_OK)



class JWTProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({"message": f"Hola, {request.user.nombre}. Tienes acceso al endpoint protegido."}, status=status.HTTP_200_OK)


class CuentaDesbloqueo(APIView):
    def post(self, request, escritura_id):
        print("ingresando a la funion de desbloqueo")
        numero_rol = request.data.get("rol_id")
        password = request.data.get("password")
        cedula = request.data.get("user_id")
        print(cedula)
        direccion_smart_contract= Escritura.objects.filter(numero_escritura=escritura_id).first().direccion_smart_contract
         
        if not cedula or not password:
            return Response({"error": "Cédula y contraseña requeridas"}, status=status.HTTP_400_BAD_REQUEST)

        user = AuthenticationService.autenticar_usuario(cedula, password)

        if user is None:
            return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)
        
        contract = SmartContract(direccion_smart_contract)
        conteo = contract.contar_validaciones()
        


        diccionario_roles = {
            4: "escribanoKey",
            5: "juezprKey",
            6: "notarioKey",
            7: "beneficiarioKey"
        }
        palabra = diccionario_roles.get(int(numero_rol), "desconocido") 
        
        print("este es el conteo ")
        print(type(numero_rol))
        print("este es el conteo")
        if conteo >=3 and int(numero_rol) == 5:
            palabra = "juezsdKey"

        credenciales = Credentials()
        key = credenciales.get_key(palabra)
        print("esta es la llave")
        print(key)
        print("print este es termino para mostrar la contraseña")
        return Response({"credential": key, "resultado_rol": palabra}) 

         

               


class RolValidacion(APIView):
    def post(self, request, escritura_id):
        numero_rol = request.data.get("role_id")
        direccion_smart_contract= Escritura.objects.filter(numero_escritura=escritura_id).first().direccion_smart_contract
        contract = SmartContract(direccion_smart_contract)
        conteo = contract.contar_validaciones()
        diccionario_roles = {
            4: "escribano",
            5: "juezpr",
            6: "notario",
            7: "beneficiario"
        }
        palabra = diccionario_roles.get(int(numero_rol), "desconocido") 
        
        if conteo >=3 and int(numero_rol) == 5:
            palabra = "juezsd"
        print("esta es la palabra")
        print(palabra)
        print("esta es la palabra")
        return Response({"resultado_rol": palabra}) 

         

               

