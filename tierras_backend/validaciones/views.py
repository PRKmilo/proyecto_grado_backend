from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notificaciones.models import Notificacion
from correcciones.models import Correcion
from escrituras.models.roles_verificadores import RolesVerificadores
from escrituras.networkService.smart_contract import SmartContract
from escrituras.networkService.credentials import Credentials
from escrituras.models.escritura import Escritura
from escrituras.models.roles_verificadores import  RolesVerificadores
from escrituras.ipfsService.ipfsService import IPFSManager
from notificaciones.notify_user import notify_user
#import cloudinary.uploader
 
from io import BytesIO
import requests
# Create your views here.

class ValidarSmartContract(APIView):
    

    def post(self, request):
        direccion_smart_contract = request.data.get("direccion_smart_contract")
        print("esta es la direccion del smart contract")
        print(direccion_smart_contract)
        respuesta_rol = request.data.get("respuesta")
        print("esta es la respuesta del rol")
        print(respuesta_rol)
        rol_validacion = request.data.get("rol")
        print("este es rol validacion")
        print(rol_validacion)
        token = request.data.get("token")
        print("esta es la token")
        print(token)
        id_user = request.data.get("id_user")
        print("este es el id_user")
        print(id_user)
        id_escritura = request.data.get("numero_escritura")
        print("esta es la id_escritura")
        print(id_escritura)
        mensaje_c = request.data.get("mensaje_correccion")
        posicion1 = request.data.get("posicion_inicial")
        posicion2 = request.data.get("posicion_final")
        print("esta es posicion1")
        print(posicion1)
        print("esta es posicion2")
        print(posicion2)
        print("mensaje")
        print(mensaje_c)
        credentials = Credentials()
        if not all([direccion_smart_contract, rol_validacion, token]):
            return Response(
                {"mensaje": "Faltan datos requeridos"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        print("linea 59")
        contract = SmartContract(direccion_smart_contract)

        roles = {
            "escribano": "escribanoKey",
            "juezpr": "juezprKey",
            "notario": "notarioKey",
            "juezsd": "juezsdKey"
        }

        if rol_validacion not in roles:
            return Response(
                {"mensaje": "Rol de validación no reconocido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        print("linea 75")
        if token != credentials.get_key(roles[rol_validacion]):
            return Response(
                {"mensaje": "Su token es incorrecto o está desactualizado"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        print("linea 81")    
        id_escribano = RolesVerificadores.objects.filter(id_escritura_id=id_escritura).first().id_escribano 
        if not respuesta_rol:
            notificacion_registro = Notificacion.objects.create(id_escritura_id=id_escritura,user_sender=id_user, user_receiver=id_escribano,mensaje=f"Tiene que corregir el documento con id #{id_escritura}")
            notify_user(notificacion_registro)
            correccion = Correcion.objects.create(id_notificacion=notificacion_registro,line_number=posicion1,start_position=posicion1,end_position=posicion2,is_resolved=False, comment=mensaje_c, descripcion=mensaje_c)

        print("linea 82")
        if not contract.contract_exist:
            return Response(
                {"mensaje": "El contrato no existe dentro de la red"},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        print("linea 95")
        # Mapeo de métodos de validación por rol
        validacion_metodos = {
            "escribano": contract.validacion_escribano,
            "juezpr": contract.validacion_juezpr,
            "notario": contract.validacion_notario,
            "juezsd": contract.valdacion_juezsd
        }
        
        print("print 104")
        instance_escritura = Escritura.objects.filter(numero_escritura=id_escritura).first()
        existe_lista_verificacion = RolesVerificadores.objects.filter(id_escritura=instance_escritura)
        validacion_metodos[rol_validacion](respuesta_rol)
        campos = {
             "escribano": {"id_escribano": id_user},
             "juezpr": {"id_juez1": id_user},
             "notario": {"id_notario": id_user},
             "juezsd": {"id_juez2": id_user}
        }
        print("liena 114")
        valores_a_guardar = campos.get(rol_validacion)
        
            
        registro = RolesVerificadores.objects.filter(id_escritura_id=id_escritura)

        if registro.exists():
            # Si existe, actualizar los valores
            if  rol_validacion == "escribano":
                registro.update(id_escribano=id_user)
                print("escribano update")
            if rol_validacion == "juezpr":
                registro.update(id_juez1=id_user)
                print("juez1 update")
            if rol_validacion == "notario":
                registro.update(id_notario=id_user)
                print("notario update")
            if rol_validacion == "juezsd":
                registro.update(id_juez2=id_user)
                print("juez2 update")
        else:
            print("No se encontró un registro con id_escritura:", id_escritura)

        print("linea 137")
        return Response(
            {"mensaje": "El proceso llegó a última instancia", "codigo": 200},
            status=status.HTTP_200_OK
        )

class ValidarBeneficiario(APIView):
    
    def post(self, request):
        token = request.data.get("token")
        respuesta = request.data.get("respuesta")
        numero_escritura = request.data.get("numero_escritura")
        mensaje_c = request.data.get("mensaje_correccion")
        posicion1 = request.data.get("posicion_inicial")
        posicion2 = request.data.get("posicion_final")
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
                    notificacion_id = Notificacion.objects.filter(id_escritura_id=escritura.numero_escritura).first()
                    Correcion.objects.filter(id_notificacion=notificacion_id.id_notificacion).update(is_resolved=True)                      
                    contract.validacion_beneficiario(respuesta,numero_escritura,nombre_notaria,fecha_otorgamiento,id_actor_otorga,id_favorecido,cedula_catastral, municipio,movimiento,CID)
                    return Response(
                       {"mensaje": "Se llego hasta la ultima instancia de la transaccion"},
                       status=status.HTTP_200_OK 
                    )
                else:

                    proceso = escritura.proceso_escritura
                    id_favorecido = id_user
                    lista_verificadores = RolesVerificadores.objects.filter(id_escritura=numero_escritura).first()
                    id_actor_otorga = lista_verificadores.id_juez2
                    cedula_catastral = escritura.cedula_catastral
                    cloudinary_url = escritura.direccion_temporal_data
                    response = requests.get(cloudinary_url)
                    file_obj = BytesIO(response.content)
                    ipfs = IPFSManager()
                    CID = ""
                    nombre_notaria = escritura.nombre_notaria
                    movimiento = escritura.descripcion_movimiento
                    municipio = escritura.municipio
                    fecha_otorgamiento = escritura.fecha_otorgamiento
                    notificacion_id = Notificacion.objects.filter(id_escritura_id=escritura.numero_escritura).first()
                    Correcion.objects.filter(id_notificacion=notificacion_id.id_notificacion).update(is_resolved=True)                      
                    id_escribano = RolesVerificadores.objects.filter(id_escritura_id=numero_escritura).first().id_escribano 

                    
                    notificacion_registro = Notificacion.objects.create(id_escritura_id=numero_escritura,user_sender=id_user, user_receiver=id_escribano,mensaje=f"Tiene que corregir el documento con id #{numero_escritura}")
                    notify_user(notificacion_registro)
                    correccion = Correcion.objects.create(id_notificacion=notificacion_registro,line_number=posicion1,start_position=posicion1,end_position=posicion2,is_resolved=False, comment=mensaje_c, descripcion=mensaje_c)
                    try:
                        contract.validacion_beneficiario(respuesta,numero_escritura,nombre_notaria,fecha_otorgamiento,id_actor_otorga,id_favorecido,cedula_catastral, municipio,movimiento,CID)


                    except Exception as e:
                        # Aquí manejamos la excepción y devolvemos una respuesta controlada
                        print("se va por el camino de error")
                        return Response({
                            "mensaje": "Transacción generada pero sin retorno",
                            "detalle": str(e)
                        }, status=status.HTTP_200_OK)  # Asegúrate de devolver una respuesta válida

                    return Response({"mensaje": "Operación exitosa"}, status=status.HTTP_200_OK)
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
