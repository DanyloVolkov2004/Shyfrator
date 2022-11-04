from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
import os 
from ciphers import ciphers
from exceptions import *


class Crypto:
    """ 
    A class used as an interface for cryptography functions
    
    A list of avaliable algorithms:
        "AES"
        "Camellia"
        "Blowfish"
        "ChaCha20" 

    After each use, either for encryption or decryption, it is crucial to generate a new instance of the class
    If None is passed as an algorithm, decryption cipher will be detected automatically for a given file but encryption will be disabled
    """

    def __init__(self, algorithm:str, password:str):
        self.name = algorithm
        self.password = password
        self.chunk_size = 65536
        self.header_size = 77

        if len(password) < 8:
            raise ShortPasswordException("Password must be 8 characters or longer")
        if algorithm is None:
            self.detect_cipher = True
            return None

        info = self.__get_info__(algorithm)
        if info == None:
            raise InvalidCipherException("There is no such cipher avaliable")
        self.__init_object_data__()

    def encrypt_file(self, source_file_path:str, destination_file_path:str):
        """method for encrypting a file, and writing the ciphertext into a separate file"""
        
        if destination_file_path == source_file_path:
            raise IdenticalSourceException("Source file path is the same as destination file path")

        source_file = open(source_file_path, "rb")
        destination_file = open(destination_file_path, "wb")
        cipher_obj = self.__init_cipher_obj__()
        encryptor = cipher_obj.encryptor()

        if self.type == "block":
            padder = self.padding_obj.padder()
        read_buffer = source_file.read(self.chunk_size)

        header = self.__generate_header__()
        destination_file.write(header)

        while len(read_buffer) == self.chunk_size:
            write_buffer = encryptor.update(read_buffer)
            destination_file.write(write_buffer)
            read_buffer = source_file.read(self.chunk_size)

        if self.type == "block":
            padded_bytes = padder.update(read_buffer) + padder.finalize()
            write_buffer = encryptor.update(padded_bytes) + encryptor.finalize()
            destination_file.write(write_buffer)
        else:
            write_buffer = encryptor.update(read_buffer) + encryptor.finalize()
            destination_file.write(write_buffer)

        source_file.close()
        destination_file.close()

    def decrypt_file(self, source_file_path:str, destination_file_path:str):
        """method for decrypting a file, and writing the ciphertext into a separate file"""

        if destination_file_path == source_file_path:
            raise IdenticalSourceException("Source file path is the same as destination file path")

        source_file = open(source_file_path, "rb")
        
        header = source_file.read(self.header_size)
        encryption_data = self.__parse_header__(header)
        # print(encryption_data)
        
        if self.detect_cipher:
            self.__init_object_data__(encryption_data)
        else:
            if self.type == "block":
                self.iv = encryption_data.get("iv")
            else:
                self.nonce = encryption_data.get("nonce") 


        # self.__validate_encryption__() 

        destination_file = open(destination_file_path, "wb")        
        cipher_obj = self.__init_cipher_obj__()
        decryptor = cipher_obj.decryptor()

        if self.type == "block":        
            unpadder = self.padding_obj.unpadder()

        first_read = True
        read_buffer = source_file.read(self.block_size)
        
        while len(read_buffer) == self.block_size:
            write_buffer = decryptor.update(read_buffer)
            read_buffer = source_file.read(self.block_size)
            if len(read_buffer) != self.block_size:
                first_read = False
                break
            destination_file.write(write_buffer)
        
        if self.type == "block":
            if first_read:
                write_buffer = decryptor.update(read_buffer) + decryptor.finalize() 
            unpadded_bytes = unpadder.update(write_buffer) + unpadder.finalize()
            destination_file.write(unpadded_bytes)
        else:
            write_buffer = decryptor.update(read_buffer) + decryptor.finalize() 
            destination_file.write(write_buffer)

        source_file.close()
        destination_file.close()

    def __init_cipher_obj__(self):
        if self.name == "AES":
            return Cipher(algorithm=algorithms.AES256(self.key), mode=modes.CBC(self.iv))
        if self.name == "Camellia":
            return Cipher(algorithm=algorithms.Camellia(self.key), mode=modes.CBC(self.iv))
        if self.name == "Blowfish":
            return Cipher(algorithm=algorithms.Blowfish(self.key), mode=modes.CBC(self.iv))
        if self.name == "ChaCha20":
            return Cipher(algorithm=algorithms.ChaCha20(self.key, self.nonce), mode=None)
        return None
        
    def __init_object_data__(self, encryption_data:dict=None):
        if encryption_data != None:
            self.name = encryption_data.get("cipher")
            self.type = encryption_data.get("type")
            self.block_size = encryption_data.get("block_size", None)
            self.nonce_size = encryption_data.get("nonce_size", None)
            if self.type == "block":
                self.iv = encryption_data.get("iv")
                self.padding_obj = padding.PKCS7(self.block_size * 8)           
            else:
                self.nonce = encryption_data["nonce"]     
        else:
            info = self.__get_info__(self.name)
            self.type = info.get("type")
            self.block_size = info.get("block_size", None)
            self.nonce_size = info.get("nonce_size", None)
            if self.type == "block":
                self.iv = self.__generate_iv__(self.block_size)
                self.padding_obj = padding.PKCS7(self.block_size * 8)
            else:
                self.nonce = self.__generate_nonce__(
                    nonce_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "nonces.txt"), 
                    nonce_length=self.nonce_size
                )       

        info = self.__get_info__(self.name)
        self.detect_cipher = False
        self.key_length = info.get("key_length")
        self.header_byte = info.get("header_byte")
        self.key = self.__generate_key__(password=self.password, key_length=self.key_length)  

    def __generate_iv__(self, iv_length:int):  
        """helper method for generating an initialization vector"""

        if iv_length == None:
            return None
        
        return os.urandom(iv_length)

    def __generate_nonce__(self, nonce_path:str, nonce_length:int):
        """helper method for generating a nonce"""

        if nonce_length == None:
            return None
        nonce_file = open(nonce_path, "rb")
        nonce = nonce_file.read()
        nonce_file.close()

        if len(nonce) != 32:
            new_nonce = os.urandom(32)
            nonce_file = open(nonce_path, "wb")            
            nonce_file.write(new_nonce)
            nonce_file.close()
            return new_nonce[32-nonce_length:]
        else:
            new_nonce = int.from_bytes(nonce, "big") + 1
            new_nonce = new_nonce.to_bytes(32, "big")
            nonce_file = open(nonce_path, "wb")            
            nonce_file.write(new_nonce)
            nonce_file.close()
            return new_nonce[32-nonce_length:]

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


    def __generate_header__(self):
        """helper method for generating encryption header"""

        header_sign = b'-4\xb6-\x8d\x12\xba\x89\x97\xcf'
        header = bytearray(header_sign)

        if self.type == "block":
            header.extend(b"\x00")
            header.extend(self.header_byte)
            header.extend(self.block_size.to_bytes(1, "big"))
            header.extend(self.iv)
            header.extend(bytes(64-self.block_size))
        else:
            header.extend(b"\x01")
            header.extend(self.header_byte)
            header.extend(self.nonce_size.to_bytes(1, "big"))
            header.extend(self.nonce)
            header.extend(bytes(64-self.nonce_size))

        return bytes(header)

    def __parse_header__(self, header:bytes):
        """helper method for parsing data from encryption header"""

        header_sign = b'-4\xb6-\x8d\x12\xba\x89\x97\xcf'
        header_head = header[0:10]

        if header_sign != header_head:
            raise InvalidHeaderSignException("This file was damaged, or not encrypted using instance of this class")

        encryption_data = {}
        cipher_type = header[10]

        if cipher_type == int.from_bytes(b"\x00", "big"):
            cipher_byte = header[11].to_bytes(1, "big")
            cipher = self.__get_cipher_from_header_byte__(cipher_byte)
            block_size = header[12]
            if block_size < 1 or block_size > 32:
                raise InvalidHeaderInfoException("Invalid block size")
            iv = header[13:(13+block_size)]

            encryption_data["type"] = "block"
            encryption_data["cipher"] = cipher
            encryption_data["block_size"] = block_size
            encryption_data["iv"] = iv

        elif cipher_type == int.from_bytes(b"\x01", "big"):
            cipher_byte = header[11].to_bytes(1, "big")
            cipher = self.__get_cipher_from_header_byte__(cipher_byte)
            nonce_size = header[12]
            if nonce_size < 1 or nonce_size > 32:
                raise InvalidHeaderInfoException("Invalid nonce size")
            nonce = header[13:(13+nonce_size)]

            encryption_data["type"] = "stream"
            encryption_data["cipher"] = cipher
            encryption_data["nonce_size"] = nonce_size
            encryption_data["nonce"] = nonce


        else:
            raise InvalidHeaderInfoException("Invalid type byte")
    
        return encryption_data

    def __validate_encryption__(self):
        """helper method for validating encryption"""
        pass

    def __get_cipher_from_header_byte__(self, cipher_byte:bytes):
        """helper method for identifying cipher from header info"""

        for (cipher, data) in ciphers.items():
            if int.from_bytes(data["header_byte"], "big") == int.from_bytes(cipher_byte, "big"):
                return cipher
        return None

    def __get_info__(self, algorithm:str):
        """helper method for getting cipher configuration information"""

        return ciphers.get(algorithm, None)

cr = Crypto("ChaCha20", "12345678")
# cr = Crypto("Camellia", "12345678")
# cr = Crypto("Camellia", "12345678")

# cr.encrypt_file("crypto/test.txt", "crypto/encryptedtest.txt")
cr.decrypt_file("crypto/encryptedtest.txt", "crypto/encryptedtestdecrypted.txt")



# cr.encrypt_file("crypto/document.docx", "crypto/encryptedtest.docx")
# cr.decrypt_file("crypto/encryptedtest.docx", "crypto/encryptedtestdecrypted.docx")