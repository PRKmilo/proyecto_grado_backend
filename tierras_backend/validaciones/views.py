from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from escrituras.networkService.smart_contract import SmartContract
from escrituras.networkService.credentials import Credentials
from escrituras.models.escritura import Escritura
from escrituras.models.roles_verificadores import  RolesVerificadores
from escrituras.ipfsService.ipfsService import IPFSManager
import cloudinary.uploader
from io import BytesIO
import requests
# Create your views here.

class ValidarSmartContract(APIView):
    

    def post(self, request):
        direccion_smart_contract = request.data.get("direccion_smart_contract")
        respuesta_rol = request.data.get("respuesta")
        rol_validacion = request.data.get("rol")
        token = request.data.get("token")
        id_user = request.data.get("id_user")
        id_escritura = request.data.get("numero_escritura")
        credentials = Credentials()
        if not all([direccion_smart_contract, respuesta_rol, rol_validacion, token]):
            return Response(
                {"mensaje": "Faltan datos requeridos"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        contract = SmartContract(direccion_smart_contract)

        roles = {
            "escribano": "escribanoKey",
            "juez1": "juezprKey",
            "notario": "notarioKey",
            "juez2": "juezsdKey"
        }

        if rol_validacion not in roles:
            return Response(
                {"mensaje": "Rol de validación no reconocido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if token != credentials.get_key(roles[rol_validacion]):
            return Response(
                {"mensaje": "Su token es incorrecto o está desactualizado"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not contract.contract_exist:
            return Response(
                {"mensaje": "El contrato no existe dentro de la red"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mapeo de métodos de validación por rol
        validacion_metodos = {
            "escribano": contract.validacion_escribano,
            "juez1": contract.validacion_juezpr,
            "notario": contract.validacion_notario,
            "juez2": contract.valdacion_juezsd
        }
        

        instance_escritura = Escritura.objects.filter(numero_escritura=id_escritura).first()
        existe_lista_verificacion = RolesVerificadores.objects.filter(id_escritura=instance_escritura)
        validacion_metodos[rol_validacion](respuesta_rol)
        campos = {
             "escribano": {"id_escribano": id_user},
             "juez1": {"id_juez1": id_user},
             "notario": {"id_notario": id_user},
             "juez2": {"id_juez2": id_user}
        }
        
        valores_a_guardar = campos.get(rol_validacion)
        
            
        registro = RolesVerificadores.objects.filter(id_escritura_id=id_escritura)

        if registro.exists():
            # Si existe, actualizar los valores
            if  rol_validacion == "escribano":
                registro.update(id_escribano=id_user)
                print("escribano update")
            if rol_validacion == "juez1":
                registro.update(id_juez1=id_user)
                print("juez1 update")
            if rol_validacion == "notario":
                registro.update(id_notario=id_user)
                print("notario update")
            if rol_validacion == "juez2":
                registro.update(id_juez2=id_user)
                print("juez2 update")
        else:
            print("No se encontró un registro con id_escritura:", id_escritura)

        return Response(
            {"mensaje": "El proceso llegó a última instancia", "codigo": 200},
            status=status.HTTP_200_OK
        )

class ValidarBeneficiario(APIView):
    
    def post(self, request):
        token = request.data.get("token")
        respuesta = request.data.get("respuesta")
        numero_escritura = request.data.get("numero_escritura")
        id_user = request.data.get("id_user")
        credentials = Credentials()
        print("recivido ")
        print(token)
        print("llave del sistema")
        print(credentials.get_key("beneficiario"))
        if token == credentials.get_key("beneficiarioKey"):
            escritura =  Escritura.objects.get(pk=numero_escritura)
            contract = SmartContract(escritura.direccion_smart_contract)
            if contract.contract_exist:
                if respuesta:
                    proceso = escritura.proceso_escritura
                    id_favorecido = id_user
                    lista_verificadores = RolesVerificadores.objects.filter(id_escritura=numero_escritura).first()
                    id_actor_otorga = lista_verificadores.id_juez2
                    cedula_catastral = escritura.cedula_catastral
                    cloudinary_url = escritura.direccion_temporal_data
                    response = requests.get(cloudinary_url)
                    file_obj = BytesIO(response.content)
                    ipfs = IPFSManager()
                    CID = ipfs.subir_archivo(file_obj)
                    nombre_notaria = escritura.nombre_notaria
                    movimiento = escritura.descripcion_movimiento
                    municipio = escritura.municipio
                    fecha_otorgamiento = escritura.fecha_otorgamiento
                    
                    contract.validacion_beneficiario(respuesta,numero_escritura,nombre_notaria,fecha_otorgamiento,id_actor_otorga,id_favorecido,cedula_catastral, municipio,movimiento,CID)
                    return Response(
                       {"mensaje": "Se llego hasta la ultima instancia de la transaccion"},
                       status=status.HTTP_200_OK 
                    )
            else:

                return Response(
                    {"mensaje": "El contrato no existe dentro de la red"},
                    status=status.HTTP_400_BAD_REQUEST
                 )  

        else:
            return Response(
                {"mensaje": "Su token es incorrecto o está desactualizado"},
                status=status.HTTP_401_UNAUTHORIZED
            )  
