import cloudinary
import cloudinary.uploader
import cloudinary.api
from decouple import config
class CloudinaryService:
    @staticmethod
    def configurar():
        """ Configura Cloudinary con las variables de entorno """
        cloudinary.config(
            cloud_name=config("cloud_name"),
            api_key=config("api_key"),
            api_secret=config("api_secret")
        )
	

    @staticmethod
    def subir_archivo(archivo, carpeta="mis_archivos"):
        """ Sube un archivo a Cloudinary y devuelve la URL """
        CloudinaryService.configurar()  # Asegurar que Cloudinary está configurado
        respuesta = cloudinary.uploader.upload(archivo, folder=carpeta)
        return respuesta.get("secure_url")  # Devuelve la URL segura del archivo

    @staticmethod
    def eliminar_archivo(public_id):
        """ Elimina un archivo de Cloudinary """
        CloudinaryService.configurar()
        respuesta = cloudinary.uploader.destroy(public_id)
        return respuesta
