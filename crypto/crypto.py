from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from .ciphers import ciphers
from .exceptions import *


class Crypto:
    """ 
    A class used as an interface for cryptography functions
    
    A list of avaliable algorithms:
        "AES"
        "Camellia"
        "Blowfish"
        
    """

    def __init__(self, algorithm:str, password:str):
        info = Crypto.__get_info__(self, algorithm)
        if info == None:
            raise InvalidCipherException("There is no such cipher avaliable") 
        if len(password) < 8:
            raise ShortPasswordException("Password must be 8 characters or longer")

        self.name = algorithm
        self.password = password
        self.key_length = info.get("key_length")
        self.block_size = info.get("block_size")
        self.chunk_size = 65536
        self.type = info.get("type")
        self.key = Crypto.__generate_key__(self, password=password, key_length=self.key_length) 

        self.cipher_obj = self.__init_cipher_obj__()
        self.padding_obj = padding.PKCS7(self.block_size * 8)
    
    def encrypt_file(self, source_file_path:str, destination_file_path:str):
        """method for encrypting a file, and writing the ciphertext into a separate file, using appropriate (selected) algorithm"""

        if destination_file_path == source_file_path:
            raise IdenticalSourceException("Source file path is the same as destination file path")

        source_file = open(source_file_path, "rb")
        destination_file = open(destination_file_path, "wb")
        encryptor = self.cipher_obj.encryptor()
        padder = self.padding_obj.padder()
        read_buffer = source_file.read(self.chunk_size)

        while len(read_buffer) == self.chunk_size:
            write_buffer = encryptor.update(read_buffer)
            destination_file.write(write_buffer)
            read_buffer = source_file.read(self.chunk_size)

        padded_bytes = padder.update(read_buffer) + padder.finalize()
        write_buffer = encryptor.update(padded_bytes) + encryptor.finalize()
        destination_file.write(write_buffer)

        source_file.close()
        destination_file.close()

    def decrypt_file(self, source_file_path:str, destination_file_path:str):
        """method for decrypting a file, and writing the plaintext content into a separate file, using appropriate (selected) algorithm"""

        if destination_file_path == source_file_path:
            raise IdenticalSourceException("Source file path is the same as destination file path")

        source_file = open(source_file_path, "rb")
        destination_file = open(destination_file_path, "wb")
        decryptor = self.cipher_obj.decryptor()
        unpadder = self.padding_obj.unpadder()
        read_buffer = source_file.read(self.chunk_size)

        while len(read_buffer) == self.chunk_size:
            write_buffer = decryptor.update(read_buffer)
            destination_file.write(write_buffer)
            read_buffer = source_file.read(self.chunk_size)

        
        write_buffer = decryptor.update(read_buffer) + decryptor.finalize() 
        unpadded_bytes = unpadder.update(write_buffer) + unpadder.finalize()
        destination_file.write(unpadded_bytes)

        source_file.close()
        destination_file.close()

    def convert_text_to_bytes(self, text):
        """method for converting text into bytes, so that you can encrypt them"""

        return bytes(text, "utf-8")

    def __init_cipher_obj__(self):
        iv = self.__generate_cbc_iv__(self.password, self.block_size)
        if self.name == "AES":
            return Cipher(algorithm=algorithms.AES256(self.key), mode=modes.CBC(iv))
        if self.name == "Camellia":
            return Cipher(algorithm=algorithms.Camellia(self.key), mode=modes.CBC(iv))
        if self.name == "Blowfish":
            return Cipher(algorithm=algorithms.Blowfish(self.key), mode=modes.CBC(iv))
        return None

    def __generate_cbc_iv__(self, password:str, iv_length:int):  
        """helper method for generating an initialization vector for CBC encryption mode"""

        str = (password*iv_length)[:iv_length] 
        return bytes(str, "utf-8")

    def __generate_key__(self, password:str, key_length:int):
        """helper method for generating key from a given password, password must be 8 characters or longer"""

        #generate salt using password
        salt = bytes(password+password, "utf-8")
        key_gen_alg = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=key_length,
            salt=salt,
            iterations=100000,
        )
        return key_gen_alg.derive(bytes(password,"utf-8"))

    def __get_info__(self, algorithm:str):
        """helper method for getting cipher configuration information"""

        return ciphers.get(algorithm, None)