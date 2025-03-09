from web3 import Web3
from decouple import config

class Web3Provider:
    _instance = None  # Almacena la única instancia

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Web3Provider, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        rpc_url = config("ALFAJORES_RPC_URL")
        if not rpc_url:
            raise ValueError("La variable de entorno ALFAJORES_RPC_URL no está definida")
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.web3.is_connected():
            raise ConnectionError("No se pudo conectar a la blockchain")

    def get_web3(self):
        return self.web3
