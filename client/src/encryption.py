from OpenSSL import crypto        
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import os

class encrypt:
    def load_public_key(self):
        with open("./otherskeys/public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        return public_key

    def generate_sym_key(self):
        return os.urandom(32)  # AES-256 key

    def encrypt_sym_key_with_public_key(self, public_key, symmetric_key):
        encrypted_symmetric_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_symmetric_key

    def read_file_to_encrypt(self):
        with open("./data/mail", 'rb') as f:
            file_data = f.read()
        return file_data

    def encrypt_file_with_sym_key(self, file_data, symmetric_key):
        # Pad and encrypt the file data using the symmetric key
        padder = sym_padding.PKCS7(128).padder() 
        padded_data = padder.update(file_data) + padder.finalize()
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(os.urandom(16)), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return encrypted_data

    def save_enc_data(self, encrypted_data):
        with open("./enc_data/mail", 'wb') as f:
            f.write(encrypted_data)

    def save_enc_sym_key(self, encrypted_symmetric_key):
        with open("./otherskeys/enc_sym_key", 'wb') as f:
            f.write(encrypted_symmetric_key)

    def run(self):
        pub_key = self.load_public_key()
        sym_key = self.generate_sym_key()
        enc_sym_key = self.encrypt_sym_key_with_public_key(pub_key, sym_key)
        file_to_enc = self.read_file_to_encrypt()
        enc_data = self.encrypt_file_with_sym_key(file_to_enc, sym_key)
        self.save_enc_data(enc_data)
        self.save_enc_sym_key(enc_sym_key)
        
        
class decrypt:
    def load_private_key(self, email):
        with open(f"./mykeys/private{email}.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        return private_key

    def load_enc_sym_key(self):
        with open("./otherskeys/enc_sym_key", 'rb') as f:
            encrypted_symmetric_key = f.read()

        return encrypted_symmetric_key

    def decrypt_sym_key(self, private_key, encrypted_symmetric_key):
        symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return symmetric_key

    def load_enc_file(self):
        with open("./enc_data/mail", 'rb') as f:
            iv = f.read(16)  # Assuming a 16-byte IV for AES
            encrypted_data = f.read()
        return iv, encrypted_data

    def decrypt_data(self, iv, symmetric_key, encrypted_data):
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        # Unpad the decrypted data
        unpadder = sym_padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(padded_data) + unpadder.finalize()
        return decrypted_data

    def run(self,email):
        priv_key = self.load_private_key(email)
        enc_sym_key = self.load_enc_sym_key()
        sym_key = self.decrypt_sym_key(priv_key, enc_sym_key)
        iv, enc_data = self.load_enc_file()
        decrypted_data = self.decrypt_data(iv, sym_key, enc_data)
        # self.save_data(decrypted_data,time)
        return decrypted_data
        

class RSA:
    def __init__(self):
        self.key = crypto.PKey()
        self.key.generate_key(crypto.TYPE_RSA, 2048)
        
    def generate_private_key(self):
        private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, self.key).decode('utf-8')
        return private_key

    def generate_public_key(self):
        public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, self.key).decode('utf-8')
        return public_key

    def save_key_priv(self, key,email):
        with open(f"./mykeys/private{email}.pem", "w") as f:
            f.write(key)
    def save_key_pub(self, key, email):
        with open(f"./mykeys/public{email}.pem", "w") as f:
            f.write(key)

    def run(self,email):
        priv_key = self.generate_private_key()
        pub_key  = self.generate_public_key()
        self.save_key_priv(priv_key,email)
        self.save_key_pub(pub_key, email)
        return pub_key