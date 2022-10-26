from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import exceptions
import ciphers


class Crypto:
    """ 
    A class used as an interface for cryptography functions
    
    A list of avaliable algorithms:
        AES

    """

    def __init__(self, algorithmm:str, password:str):
        info = Crypto.__get_info__(self, algorithmm)
        if info == None:
            raise exceptions.InvalidCipherException("There is no such cipher avaliable") 
        if len(password) < 8:
            raise exceptions.ShortPasswordException("Password must be 8 characters or longer")

        self.name = algorithmm
        self.key_length = info.get("key_length")
        self.type = info.get("type")
        self.key = Crypto.__generate_key__(self, password=password, key_length=self.key_length)
    

    def encrypt(self, bytes:bytes):
        """method for encrypting generic bytes, using appropriate (selected) algorithm"""

        if self.name == "AES":
            return self.__encrypt_aes__(bytes)
        else:
            raise exceptions.InvalidCipherException("There is no such cipher avaliable") 

    def decrypt(self, bytes:bytes):
        """method for decrypting generic bytes, using appropriate (selected) algorithm"""

        if self.name == "AES":
            return self.__decrypt_aes__(bytes)
        else:
            raise exceptions.InvalidCipherException("There is no such cipher avaliable") 

    def convert_text_to_bytes(self, text):
        """method for converting text into bytes, so that you can encrypt them"""

        return bytes(text, "utf-8")

    
    def __generate_key__(self, password:str, key_length:int):
        """method for generating key from a given password, must be longer than 8"""

        #generate salt using password
        salt = bytes(password+password, "utf-8")
        key_gen_alg = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=key_length,
            salt=salt,
            iterations=10000,
        )
        return key_gen_alg.derive(bytes(password,"utf-8"))

    def __get_info__(self, algorithm:str):
        """method for getting information about the cipher"""

        return ciphers.ciphers.get(algorithm, None)



