from cryptography.fernet import Fernet, InvalidToken
import hashlib
import math
import os

from Crypto.Cipher import AES

IV_SIZE = 16
KEY_SIZE = 32
SALT_SIZE = 16


class InvalidKey(Exception):
    pass


def decrypt(encrypted: bytes, key: bytes) -> str:
    f = Fernet(key)

    try:
        decrypted = f.decrypt(encrypted)
    except InvalidToken:
        raise InvalidKey()

    return decrypted.decode()


def encrypt(data: str, key: bytes) -> bytes:
    f = Fernet(key)

    return f.encrypt(data.encode())


def generate_cert(password: str) -> bytes:
    encoded_password = password.encode()
    cert = Fernet.generate_key()

    salt = os.urandom(SALT_SIZE)
    derived = hashlib.pbkdf2_hmac(
        "sha256", encoded_password, salt, 100000, dklen=IV_SIZE + KEY_SIZE
    )
    iv = derived[0:IV_SIZE]
    key = derived[IV_SIZE:]

    encrypted = salt + AES.new(key, AES.MODE_CFB, iv).encrypt(cert)
    return encrypted


def decrypt_cert(encrypted: bytes, password: str) -> bytes:
    encoded_password = password.encode()
    salt = encrypted[0:SALT_SIZE]
    derived = hashlib.pbkdf2_hmac(
        "sha256", encoded_password, salt, 100000, dklen=IV_SIZE + KEY_SIZE
    )
    iv = derived[0:IV_SIZE]
    key = derived[IV_SIZE:]
    cleartext = AES.new(key, AES.MODE_CFB, iv).decrypt(encrypted[SALT_SIZE:])
    return cleartext
