from django.shortcuts import render
from .networkService.middelwareNetwork import middelwareNetworkService 
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Escritura
from .serializers import EscrituraSerializer
from firebase.firebaseService import FirebaseService
from rest_framework.parsers import MultiPartParser, FormParser
from .models import RolesVerificadores
from rest_framework.permissions import IsAuthenticated
from escrituras.networkService.smart_contract import SmartContract
from notificaciones.notificaciones_service import NotificacionesService
class EscrituraListCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    """
    GET: Listar todos las escrituras
    POST: Crear un nuevo escritura
    """
    def get(self, request):
        permission_classes = [IsAuthenticated]
        escrituras = Escritura.objects.all()
        serializer = EscrituraSerializer(escrituras, many=True)
        return Response(serializer.data)

    def post(self, request):
        #permission_classes = [IsAuthenticated]
        #serializer = EscrituraSerializer(data=request.data)
        #request.data['direccion_smart_contract'] = middelwareNetworkService.deploy_contrac()
        archivo_txt = request.FILES.get('archivo_txt')
        archivo_pdf = request.FILES.get('archivo_pdf')
        print(request.data)
        firebase = FirebaseService()
        url2 = ''
        if archivo_txt:
            try:
                url = firebase.subir_archivo(archivo_txt)
                if archivo_pdf:
                    url2 = firebase.subir_archivo(archivo_pdf)
            except Exception as e:
                return Response({"error": f"Error al subir el archivo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            url_pdf = None   

        request.data['direccion_temporal_data'] = url
        request.data['direccion_temporal_data2'] = url2
        request.data['direccion_smart_contract'] = middelwareNetworkService.deploy_contrac()
        serializer = EscrituraSerializer(data=request.data)
        if serializer.is_valid():
            escritura=serializer.save()

            registro = RolesVerificadores.objects.create(id_escritura=escritura)
            NotificacionesService.generar_seleccion_aleatoria(request.data['user_id'], request.data['beneficiario_id'], escritura.numero_escritura, registro)
            print("Registro creado:", registro)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EscrituraUpdateView(APIView):
    """
    GET: Obtener una escritura por ID
    PUT: Actualizar un escritura existente
    """
    def get(self, request, escritura_id):
        permission_classes = [IsAuthenticated]
        try:
            escritura = Escritura.objects.get(pk=proceso_id)
            serializer = EscrituraSerializer(escritura)
            return Response(serializer.data)
        except Escritura.DoesNotExist:
            return Response({'error': 'Escritura no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, escritura_id):
        #permission_classes = [IsAuthenticated]
        archivo_txt = request.FILES.get('archivo_txt')
        archivo_pdf = request.FILES.get('archivo_pdf')
        print(request.data)
        try:
            escritura = Escritura.objects.get(pk=escritura_id)
        except Escritura.DoesNotExist:
            return Response({'error': 'Escritura no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        firebase = FirebaseService()
        url2 = ''
        if archivo_txt:
            try:
                url = firebase.subir_archivo(archivo_txt)
                if archivo_pdf:
                    url2 = firebase.subir_archivo(archivo_pdf)
            except Exception as e:
                return Response({"error": f"Error al subir el archivo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            url_pdf = None   
        escritura.direccion_temporal_data = url
        escritura.direccion_temporal_data2 = url2

        escritura.save(update_fields=['direccion_temporal_data', 'direccion_temporal_data2'])
        serializer = EscrituraSerializer(escritura)
        return Response(serializer.data,  status=status.HTTP_200_OK)

class EscrituraConsultaEtapa(APIView):
    def get(self, request, escritura_id):
    
        print("este es -------------------------------------------------------------------------- 1")
        direccion_smart_contract = Escritura.objects.filter(numero_escritura= escritura_id).first().direccion_smart_contract
        
        print("este es -------------------------------------------------------------------------- 1")
        print("este es -------------------------------------------------------------------------- 2")
        print(direccion_smart_contract)
        contract = SmartContract(direccion_smart_contract)
        
        print("este es -------------------------------------------------------------------------- 3")
        validaciones = contract.contar_validaciones()
        print(type(validaciones))
        print("esta son las validaciones")
        print(validaciones)
        print("esta son las validaciones")
        return Response(int(validaciones))


class EscrituraActualizacionPdf(APIView):
    def put(self, request, escritura_id):
        file_pdf = request.data.get("pdf")
        
        try:
            escritura = Escritura.objects.get(pk=escritura_id)
        except Escritura.DoesNotExist:
            return Response({'error': 'Escritura no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        firebase = FirebaseService()
        if file_pdf:
            try:
                url = firebase.subir_archivo(file_pdf)
            except Exception as e:
                return Response({"error": f"Error al subir el archivo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            url_pdf = None   
         
        escritura.direccion_temporal_data = url
        escritura.save(update_fields=['direccion_temporal_data'])
        serializer = EscrituraSerializer(escritura)
        return Response(serializer.data,  status=status.HTTP_200_OK)
