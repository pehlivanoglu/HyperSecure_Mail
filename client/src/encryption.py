from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
import os
from OpenSSL import crypto        

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

    def save_key(self, key, filename):
        with open(f"../Key-Pairs/{filename}.pem", "w") as f:
            f.write(key)

    def run(self):
        priv_key = self.generate_private_key()
        pub_key  = self.generate_public_key()
        self.save_key(priv_key, "private_key")
        self.save_key(pub_key, "public_key")

class encrypt:
    
    def load_public_key(self, file_path):
        with open(file_path, "rb") as key_file:
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

    def read_file_to_encrypt(self, file_path):
        with open(file_path, 'rb') as f:
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
        with open("../Key-Pairs/enc_file", 'wb') as f:
            f.write(encrypted_data)

    def save_enc_sym_key(self, encrypted_symmetric_key):
        with open("../Key-Pairs/sym_key", 'wb') as f:
            f.write(encrypted_symmetric_key)

    def run(self, public_key_path, file_to_enc_path):
        pub_key = self.load_public_key(public_key_path)
        sym_key = self.generate_sym_key()
        enc_sym_key = self.encrypt_sym_key_with_public_key(pub_key, sym_key)
        file_to_enc = self.read_file_to_encrypt(file_to_enc_path)
        enc_data = self.encrypt_file_with_sym_key(file_to_enc, sym_key)
        self.save_enc_data(enc_data)
        self.save_enc_sym_key(enc_sym_key)
        
        

class decrypt:
    def load_private_key(self, file_path):
        with open(file_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        return private_key

    def load_enc_sym_key(self, file_path):
        with open(file_path, 'rb') as f:
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

    def load_enc_file(self, file_path):
        with open(file_path, 'rb') as f:
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

    def save_data(self, file_path, decrypt_data):
        with open(file_path, 'wb') as f:
            f.write(decrypt_data)

    def run(self, private_key_path, enc_symmetric_key_path, encrypted_file_path, write_to_file = False, file_to_write_path=""):
        priv_key = self.load_private_key(private_key_path)
        enc_sym_key = self.load_enc_sym_key(enc_symmetric_key_path)
        sym_key = self.decrypt_sym_key(priv_key, enc_sym_key)
        iv, enc_data = self.load_enc_file(encrypted_file_path)
        decrypted_data = self.decrypt_data(iv, sym_key, enc_data)
        
        if write_to_file:
            if(file_to_write_path==""):
                print("You must provide a path to write the decrypted file!")
            else:
                self.save_data(file_to_write_path, decrypted_data)
        else:
            return decrypted_data
        


