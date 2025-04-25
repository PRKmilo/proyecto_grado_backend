import os
import firebase_admin
from firebase_admin import credentials, storage
import requests
import uuid
import pdb



class FirebaseService:
    def __init__(self):
        # Ruta al archivo JSON de credenciales (en la misma carpeta)
        print("-------- inside of firebase_service  1")
        cred_path = os.path.join(os.path.dirname(__file__), 'proyectoprueba-46431-firebase-adminsdk-fbsvc-4175e4c6ec.json')
        print("-------- inside of firebase_service  2")

        if not firebase_admin._apps:
            print("-------- inside of firebase_service  3")
            cred = credentials.Certificate(cred_path)
            print("-------- inside of firebase_service  4")
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'proyectoprueba-46431.firebasestorage.app'  # Cambia esto por el ID real de tu bucket
            })
            print("-------- inside of firebase_service  5")

        self.bucket = storage.bucket()
        print("-------- inside of firebase_service  6")

    def subir_archivo(self, archivo):
        """
        Sube un archivo a Firebase Storage.

        :param archivo: Archivo recibido (por ejemplo, desde Django request.FILES['archivo'])
        :param nombre_destino: Nombre con el que se guardará en el bucket
        :return: URL pública del archivo
        """
        print("-------- inside of subir_archivo  1")
        extension = os.path.splitext(archivo.name)[1]
        print("-------- inside of subir_archivo  2")
        nombre_generado = f"{uuid.uuid4().hex}{extension}"
        print("-------- inside of subir_archivo  3")
        ruta_completa = f"escrituras/{nombre_generado}"

        print("-------- inside of subir_archivo  4")
        # Subida del archivo
        blob = self.bucket.blob(ruta_completa)
        print("-------- inside of subir_archivo  5")
        blob.upload_from_file(archivo, content_type=archivo.content_type)
        print("-------- inside of subir_archivo  6")
        blob.make_public()

        return blob.public_url

    def obtener_documento_desde_url(self, url_archivo):
        """
        Descarga el contenido de un archivo desde su URL pública en Firebase Storage.

        :param url_archivo: URL pública del archivo
        :return: contenido binario del archivo o None si hubo error
        """
        try:
            respuesta = requests.get(url_archivo)
            if respuesta.status_code == 200:
                return respuesta.content
            else:
                print(f"Error al descargar archivo: {respuesta.status_code}")
                return None
        except Exception as e:
            print(f"Excepción al descargar archivo: {e}")
            return None
