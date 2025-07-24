import os
from cryptography.fernet import Fernet

KEY_FILE = 'secret.key'


def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key


def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    return None


def encrypt_folder(folder_path, key):
    fernet = Fernet(key)
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                data = f.read()
            encrypted = fernet.encrypt(data)
            with open(file_path, 'wb') as f:
                f.write(encrypted)


def decrypt_folder(folder_path, key):
    fernet = Fernet(key)
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                data = f.read()
            try:
                decrypted = fernet.decrypt(data)
                with open(file_path, 'wb') as f:
                    f.write(decrypted)
            except Exception:
                pass  # skip files that are not encrypted
