from .middelwareNetwork  import middelwareNetworkService
from .credentials import Credentials
from datetime import datetime

class SmartContract:
     
    def __init__(self, direction):
        self.direction = direction
        self.files = middelwareNetworkService.load_abi_bytecode("escrituras/networkService/contracs/abi_contract.json","escrituras/networkService/contracs/bytecode_contract.json")

    def instance(self):
        return middelwareNetworkService.instance_contract(self.direction, self.files[0])
   

    def contract_exist(self):
        return middelwareNetworkService.is_contract_active(self.direction)
    
    def validacion_escribano(self,validation):
        credentials = Credentials()
        print("transaccion escribano")
        transaction = self.instance().functions.escribanoApproved(validation).build_transaction({
                                'from' : credentials.get_role("escribano"),
                                'nonce': middelwareNetworkService.nonce(credentials.get_role("escribano")),})

        middelwareNetworkService.transaction(self.instance(), transaction, credentials.get_key("escribanoKey")) 

    def validacion_juezpr(self,validation):
        credentials = Credentials()
        print("transaccion juez 1")
        transaction = self.instance().functions.juezprApproved(validation).build_transaction({
                                'from' : credentials.get_role("juezpr"),
                                'nonce': middelwareNetworkService.nonce(credentials.get_role("juezpr")),})

        middelwareNetworkService.transaction(self.instance(), transaction, credentials.get_key("juezprKey")) 

    def validacion_notario(self, validation):
        credentials = Credentials()
        print("transaccion notario")
        transaction = self.instance().functions.notarioApproved(validation).build_transaction({
                                'from' : credentials.get_role("notario"),
                                'nonce': middelwareNetworkService.nonce(credentials.get_role("notario")),})

        middelwareNetworkService.transaction(self.instance(), transaction, credentials.get_key("notarioKey")) 

    def valdacion_juezsd(self, validation):
        credentials = Credentials()
        print("transaccion juez 2")
        transaction = self.instance().functions.juezsdApproved(validation).build_transaction({
                                'from' : credentials.get_role("juezsd"),
                                'nonce': middelwareNetworkService.nonce(credentials.get_role("juezsd")),})

        middelwareNetworkService.transaction(self.instance(), transaction, credentials.get_key("juezsdKey")) 

    def validacion_beneficiario(self,aprove,numero_escritura,nombre_notaria,fecha_otorgamiento,actor_otorga, actor_afavor,cedula_catastral, municipio, movimiento, dir_ipfs):
        credentials = Credentials()
        print("transaccion beneficiario")
        print(f"aprobacion: {aprove}")
        print(f"numero de escritura: {numero_escritura}")
        print(f"nombre_notaria: {nombre_notaria}")
        print(f"fecha de otorgamiento: {fecha_otorgamiento}")
        print(f"actor otorga: {actor_otorga}")
        print(f"actor a favor: {actor_afavor}")
        print(f"cedula catastral: {cedula_catastral}")
        print(f"municipio: {municipio}")
        print(f"movimiento: {movimiento}")
        print(f"dir_ipfs: {dir_ipfs}")
        date_uint= int(datetime.combine(fecha_otorgamiento, datetime.min.time()).timestamp())
        transaction = self.instance().functions.beneficiarioApproved(aprove, numero_escritura, nombre_notaria, date_uint, actor_otorga, actor_afavor, cedula_catastral, municipio, movimiento, dir_ipfs).build_transaction({
                                'from' : credentials.get_role("beneficiario"),
                                'nonce': middelwareNetworkService.nonce(credentials.get_role("beneficiario")),})

        middelwareNetworkService.transaction(self.instance(), transaction, credentials.get_key("beneficiarioKey")) 

    def contar_validaciones(self):
        value = self.instance().functions.contarAprobaciones().call()
        return value 

