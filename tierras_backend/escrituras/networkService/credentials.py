from decouple import config

class Credentials:
    _instance = None  # Variable para almacenar la instancia única

    def __new__(cls):
        """Garantiza que solo haya una instancia de la clase."""
        if cls._instance is None:
            cls._instance = super(Credentials, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Carga las variables de entorno una sola vez al inicializar."""
        self.ADMIN  = config("PUBLIC_ADDRESS_MAIN_ACCOUNT")
        self.ESCRIBANO = config("DIR_ESCRIBANO")
        self.JUEZPR = config("DIR_JUEZPR")
        self.NOTARIO = config("DIR_NOTARIO")
        self.JUEZSD = config("DIR_JUEZSD")
        self.BENEFICIARIO = config("DIR_BENEFICIARIO")
        self.RPC_URL = config("ALFAJORES_RPC_URL")

        self.roles = {
            "admin" :  self.ADMIN,
            "escribano": self.ESCRIBANO,
            "juezpr": self.JUEZPR,
            "notario": self.NOTARIO,
            "juezsd": self.JUEZSD,
            "beneficiario": self.BENEFICIARIO,
        }
        self.AdminKey = config("PRIVATE_KEY_ADMIN_ACCOUNT")
        self.EscribanoKey = config("PRIVATE_KEY_ESCRIBANO")
        self.JuezprKey = config("PRIVATE_KEY_JUEZPR")
        self.NotarioKey = config("PRIVATE_KEY_NOTARIO")
        self.JuezsdKey = config("PRIVATE_KEY_JUEZSD")
        self.BeneficiarioKey = config("PRIVATE_KEY_BENEFICIARIO")

        self.keys = {
             "adminKey" :  self.AdminKey,
             "escribanoKey": self.EscribanoKey,
             "juezprKey" : self.JuezprKey,
             "notarioKey" : self.NotarioKey,
             "juezsdKey" : self.JuezsdKey,
             "beneficiarioKey" : self.BeneficiarioKey
        }
      
    def get_role(self, role):
        """Devuelve la dirección de un rol específico."""
        return self.roles.get(role, None)

    def get_key(self, role):
        return self.keys.get(role, None)
    
    def get_roles(self):
        return self.roles
