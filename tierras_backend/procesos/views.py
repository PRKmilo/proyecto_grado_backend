from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Proceso
from .serializers import ProcesoSerializer
from rest_framework.permissions import IsAuthenticated
from escrituras.models import Escritura
from escrituras.serializers import  EscrituraSerializer

class ProcesoListCreateView(APIView):
    """
    GET: Listar todos los procesos
    POST: Crear un nuevo proceso
    """
    def get(self, request):
        permission_classes = [IsAuthenticated]
        procesos = Proceso.objects.all()
        serializer = ProcesoSerializer(procesos, many=True)
        return Response(serializer.data)

    def post(self, request):
        permission_classes = [IsAuthenticated]
        serializer = ProcesoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProcesoUpdateView(APIView):
    """
    GET: Obtener un proceso por ID
    PUT: Actualizar un proceso existente
    """
    def get(self, request, proceso_id):
        permission_classes = [IsAuthenticated]
        try:
            proceso = Proceso.objects.get(pk=proceso_id)
            serializer = ProcesoSerializer(proceso)
            return Response(serializer.data)
        except Proceso.DoesNotExist:
            return Response({'error': 'Proceso no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, proceso_id):
        permission_classes = [IsAuthenticated]
        try:
            proceso = Proceso.objects.get(pk=proceso_id)
        except Proceso.DoesNotExist:
            return Response({'error': 'Proceso no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProcesoSerializer(proceso, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProcesoEscritura(APIView):

    def get(self, request, proceso_id):
        lista_escrituras = Escritura.objects.filter(proceso_escritura= proceso_id)
        serializer= EscrituraSerializer(lista_escrituras, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
 

