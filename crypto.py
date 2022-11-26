from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
import exceptions
import ciphers
import os


class Crypto:
    """ 
    A class used as an interface for cryptography functions
    
    A list of avaliable algorithms:
        "AES"
        "Camellia"
        "Blowfish"
        "ChaCha20" 

    If None is passed as an algorithm, decryption cipher will be detected automatically for a given file but encryption will be disabled
    """

    def __init__(self, algorithm:str, password:str):
        self.name = algorithm
        self.password = password
        self.chunk_size = 65536
        self.header_size = 76
        self.hmac_size = 32

        if len(password) < 8:
            raise exceptions.ShortPasswordException("Password must be 8 characters or longer")

        info = self.__get_info__(algorithm)
        if info == None:
            raise exceptions.InvalidCipherException("There is no such cipher avaliable")
        self.type = info.get("type")
        self.block_size = info.get("block_size", None)
        self.nonce_size = info.get("nonce_size", None)
        if self.type == "block":
            self.padding_obj = padding.PKCS7(self.block_size * 8)

        self.key_length = info.get("key_length")
        self.key = self.__generate_key__(password=self.password, key_length=self.key_length) 

    def encrypt_file(self, source_file_path:str, destination_file_path:str):
        """method for encrypting a file, and writing the ciphertext into a separate file"""
        
        if destination_file_path == source_file_path:
            raise exceptions.IdenticalSourceException("Source file path is the same as destination file path")

        self.__init_new_encryption_data__()

        source_file = open(source_file_path, "rb")
        destination_file = open(destination_file_path, "wb")
        cipher_obj = self.__init_cipher_obj__()
        encryptor = cipher_obj.encryptor()
        hmac = HMAC(key=self.key, algorithm=hashes.SHA256())

        if self.type == "block":
            padder = self.padding_obj.padder()

        header = self.__generate_header__()
        destination_file.write(header)
        hmac.update(header)
        read_buffer = source_file.read(self.chunk_size)

        while len(read_buffer) == self.chunk_size:
            write_buffer = encryptor.update(read_buffer)
            hmac.update(write_buffer)
            destination_file.write(write_buffer)
            read_buffer = source_file.read(self.chunk_size)

        if self.type == "block":
            padded_bytes = padder.update(read_buffer) + padder.finalize()
            write_buffer = encryptor.update(padded_bytes) + encryptor.finalize()
            destination_file.write(write_buffer)
        else:
            write_buffer = encryptor.update(read_buffer) + encryptor.finalize()
            destination_file.write(write_buffer)
    
        hmac.update(write_buffer)
        signature = hmac.finalize()
        destination_file.write(signature)
        source_file.close()
        destination_file.close()

    def decrypt_file(self, source_file_path:str, destination_file_path:str):
        """method for decrypting a file, and writing the ciphertext into a separate file"""

        if destination_file_path == source_file_path:
            raise exceptions.IdenticalSourceException("Source file path is the same as destination file path")

        self.__init_decryption_data_from_file_header__(source_file_path)
        self.__authenticate_decryption__(source_file_path)

        source_file = open(source_file_path, "rb")
        source_file.seek(0, 2)
        file_length = source_file.tell()
        source_file.seek(self.header_size, 0)
        destination_file = open(destination_file_path, "wb")      
        try:
            cipher_obj = self.__init_cipher_obj__()
        except:
            raise exceptions.DecryptionFailException("Invalid decryption parameters")
        decryptor = cipher_obj.decryptor()

        if self.type == "block":        
            unpadder = self.padding_obj.unpadder()

        first_read = True
        while file_length - source_file.tell() > self.chunk_size + self.hmac_size:
            read_buffer = source_file.read(self.chunk_size)
            write_buffer = decryptor.update(read_buffer)
            destination_file.write(write_buffer)
            if len(read_buffer) != self.chunk_size:
                first_read = False
                break        

        read_buffer = source_file.read()
        if self.type == "block":
            if first_read:
                write_buffer = decryptor.update(read_buffer[:-self.hmac_size]) + decryptor.finalize()
            unpadded_bytes = unpadder.update(write_buffer) + unpadder.finalize()
            destination_file.write(unpadded_bytes)
        else:
            write_buffer = decryptor.update(read_buffer[:-self.hmac_size]) + decryptor.finalize() 
            destination_file.write(write_buffer)

        source_file.close()
        destination_file.close()

    def __init_cipher_obj__(self):
        """helper method for initiating cipher object"""

        if self.name == "AES":  
            return Cipher(algorithm=algorithms.AES256(self.key), mode=modes.CBC(self.iv))
        if self.name == "Camellia":
            return Cipher(algorithm=algorithms.Camellia(self.key), mode=modes.CBC(self.iv))
        if self.name == "Blowfish":
            return Cipher(algorithm=algorithms.Blowfish(self.key), mode=modes.CBC(self.iv))
        if self.name == "ChaCha20":
            return Cipher(algorithm=algorithms.ChaCha20(self.key, self.nonce), mode=None)
        return None

    def __init_new_encryption_data__(self):
        """helper method for initiating encryption data for a new encryption session"""

        if self.type == "block":
            self.iv = self.__generate_iv__(self.block_size)
        else:
            self.nonce = self.__generate_nonce__(
                nonce_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "nonces.txt"), 
                nonce_length=self.nonce_size
            )

    def __init_decryption_data_from_file_header__(self, source_file_path:str):
        """helper method for initiating decryption data from file header"""

        source_file = open(source_file_path, "rb")
        header = source_file.read(self.header_size)
        encryption_data = self.__parse_header__(header)

        self.iv = encryption_data.get("iv", None)
        self.nonce = encryption_data.get("nonce", None) 

    def __generate_iv__(self, iv_length:int):  
        """helper method for generating an initialization vector"""

        if iv_length == None:
            return None
        
        return os.urandom(iv_length)

    def __generate_nonce__(self, nonce_path:str, nonce_length:int):
        """helper method for generating a nonce"""

        if nonce_length == None:
            return None
        if not os.path.isfile(nonce_path):
            nonce_file = open(nonce_path, "wb")
            nonce_file.close()
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
            header.extend(self.block_size.to_bytes(1, "big"))
            header.extend(self.iv)
            header.extend(bytes(64-self.block_size))
        else:
            header.extend(b"\x01")
            header.extend(self.nonce_size.to_bytes(1, "big"))
            header.extend(self.nonce)
            header.extend(bytes(64-self.nonce_size))

        return bytes(header)

    def __parse_header__(self, header:bytes):
        """helper method for parsing data from encryption header"""

        header_sign = b'-4\xb6-\x8d\x12\xba\x89\x97\xcf'
        header_head = header[0:10]

        if header_sign != header_head:
            raise exceptions.InvalidHeaderSignException("This file was damaged, or not encrypted using instance of this class")

        encryption_data = {}
        cipher_type = header[10]

        if cipher_type == int.from_bytes(b"\x00", "big"):
            block_size = header[11]
            if block_size < 1 or block_size > 32:
                raise exceptions.InvalidHeaderInfoException("Invalid block size")
            iv = header[12:(12+block_size)]

            encryption_data["type"] = "block"
            encryption_data["block_size"] = block_size
            encryption_data["iv"] = iv

        elif cipher_type == int.from_bytes(b"\x01", "big"):
            nonce_size = header[11]
            if nonce_size < 1 or nonce_size > 32:
                raise exceptions.InvalidHeaderInfoException("Invalid nonce size")
                
            nonce = header[12:(12+nonce_size)]
            encryption_data["type"] = "stream"
            encryption_data["nonce_size"] = nonce_size
            encryption_data["nonce"] = nonce
        else:
            raise exceptions.InvalidHeaderInfoException("Invalid type byte")
    
        return encryption_data

    def __authenticate_decryption__(self, file_path:str):
        """helper method for decryption autentication"""

        file = open(file_path, "rb")
        file.seek(-self.hmac_size, 2)
        hmac_signature = file.read(self.hmac_size)
        file_length = file.tell() + self.hmac_size
        file.seek(0)
        hmac = HMAC(key=self.key, algorithm=hashes.SHA256())

        while file_length - file.tell() > self.chunk_size + self.hmac_size:
            read_buffer = file.read(self.chunk_size)
            hmac.update(read_buffer)

        read_buffer = file.read()
        hmac.update(read_buffer[:-self.hmac_size])
        computed_hmac = hmac.finalize()
        
        if computed_hmac != hmac_signature:
            file.close()
            raise exceptions.DecryptionFailException("File signature did not match recomputed signature")
        file.close()

    def __get_info__(self, algorithm:str):
        """helper method for getting cipher configuration information"""

        return ciphers.ciphers.get(algorithm, None)