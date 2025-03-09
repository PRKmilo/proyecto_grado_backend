from django.shortcuts import render
from models import Notificacion
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from serializers import NotificacionSerializer


class NotificacionCreateView(APIView):
      
    def get(self, request, notificacion_id):
        try:
            notificacion = Notificacion.object.get(pk=notificacion_id)
            serializar = NotificacionSerializers(notificacion)
            return Response(serializer.data)
        except Notificacion.DoesNotExist:
            return Response({'error': 'Notificacion no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        serializer = NotificacionSerializer(data=request.data)
        if serializer.is_valid():
            notificacion=serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class NotificacionListUser(APIView):
    
    def get(self, request, user_id):
        try:
            notificaciones = Notificacion.objects.filter(user_receiver=user_id)
            
            serializer = NotificacionSerializer(notificaciones, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
