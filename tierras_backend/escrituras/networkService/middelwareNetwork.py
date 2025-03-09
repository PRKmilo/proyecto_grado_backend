
import time 
import json 
from .credentials import Credentials
from .web3Provider import Web3Provider

class middelwareNetworkService:
    
    @staticmethod
    def nonce(address_transaction):
        return Web3Provider().get_web3().eth.get_transaction_count(address_transaction)
    

   
    @staticmethod
    def load_abi_bytecode(abi_file, bytecode_file):
        with open(abi_file, "r") as abi_fp:
            abi = json.load(abi_fp)
        with open(bytecode_file, "r") as file:
            bytecode = file.read().strip()
        return abi, bytecode

    @staticmethod
    def gas_price():
        return Web3Provider().get_web3().eth.gas_price 
    
    @staticmethod
    def deploy_contrac():
        credentials = Credentials()  # 🔹 Crear instancia de la clase
        addresses = list(credentials.get_roles().values())  
        public_address_deployer = credentials.get_role("admin")  
        private_key_deployer = credentials.get_key("adminKey")  
        gas_price = middelwareNetworkService().gas_price()
        if len(addresses) != 6:
            raise ValueError("Se debe proporcionar exactamente 6 direcciones")
        contract_abi, contract_bytecode = middelwareNetworkService.load_abi_bytecode("escrituras/networkService/contracs/abi_contract.json", "escrituras/networkService/contracs/bytecode_contract.json")
        contract = Web3Provider().get_web3().eth.contract(abi=contract_abi, bytecode= contract_bytecode)
        nonce= middelwareNetworkService.nonce(public_address_deployer)
        simulated_deploy= contract.constructor(*addresses).build_transaction({
         'from': public_address_deployer,
         'nonce': nonce })
        gas_estimated = Web3Provider().get_web3().eth.estimate_gas(simulated_deploy)
        transaction = contract.constructor(*addresses).build_transaction({
            "chainId": 44787,  # ID de Alfajores
            "gas": int(gas_estimated * 1.2),
            "gasPrice": gas_price,
            "nonce": nonce,
         })

        signed_tx = Web3Provider().get_web3().eth.account.sign_transaction(transaction, private_key_deployer)
        tx_hash = Web3Provider().get_web3().eth.send_raw_transaction(signed_tx.raw_transaction)

        print(f"Esperando confirmación de la transacción: {Web3Provider().get_web3().to_hex(tx_hash)}")
        tx_receipt = Web3Provider().get_web3().eth.wait_for_transaction_receipt(tx_hash)

        print(f"Contrato desplegado en: {tx_receipt.contractAddress}")
        return tx_receipt.contractAddress

    @staticmethod
    def transaction(contract, build_transaction, key):
        try:
            print("transaccion")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print(build_transaction)
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            gas_estimated = Web3Provider().get_web3().eth.estimate_gas(build_transaction)
            print(f"gas estimado: {gas_estimated}")
            build_transaction['gas'] = int(gas_estimated * 1.2)
            signed_tx = Web3Provider().get_web3().eth.account.sign_transaction(build_transaction, key)
            tx_hash = Web3Provider().get_web3().eth.send_raw_transaction(signed_tx.raw_transaction)
            #COUNT= COUNT + 1
            print(f"transaccion de validacion: {tx_hash}")
            #print(COUNT)
            return tx_hash.hex()
        except Exception as e:
            print("error 000000000000000000000000000000000000000000000")
            print(f"error en transaccion : {e}")
     
    @staticmethod
    def instance_contract(direction, abi):
        return Web3Provider().get_web3().eth.contract(address=direction, abi = abi)
  
    @staticmethod
    def is_contract_active(address):
        """ Verifica si una dirección tiene un contrato activo en la blockchain. """
        if not Web3Provider().get_web3().is_address(address):
            raise ValueError(f"La dirección {address} no es válida")

        code = Web3Provider().get_web3().eth.get_code(address)  # Obtiene el bytecode del contrato
        if code and code != b'' and code != '0x':  # Si hay código, el contrato está activo
            return True
        return False   

