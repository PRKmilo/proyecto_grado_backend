import requests

class IPFSManager:
    def __init__(self, api_url="http://127.0.0.1:5001/api/v0"):
        self.api_url = api_url  # URL de la API de IPFS local

    def subir_archivo(self, file_obj):
        """Sube un archivo a IPFS desde un objeto en memoria y devuelve su hash CID"""
        files = {'file': ('archivo', file_obj.read())}  # Enviar el archivo
        response = requests.post(f"{self.api_url}/add", files=files)

        if response.status_code == 200:
            return response.json()["Hash"]  # Devuelve el CID del archivo
        else:
            raise Exception(f"Error al subir a IPFS: {response.text}")

