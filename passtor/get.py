import pyperclip
import time

from typing import Optional
from multiprocessing import Process

from .encrypt import decrypt, encrypt
from .store import Storage


def copy_to_cliboard(data: str, expires: Optional[int] = None) -> None:
    old_clipboard = pyperclip.paste()
    pyperclip.copy(data)

    if expires is not None:
        time.sleep(expires)
        pyperclip.copy(old_clipboard)


def get_password(
    storage: Storage, key: str, password: bytes, expires: Optional[int] = None
) -> str:
    encrypted = storage.fetch(key)
    decrypted = decrypt(encrypted, password)
    p = Process(target=copy_to_cliboard, args=(decrypted, expires))
    p.start()
    return decrypted


def store_password(storage: Storage, key: str, password: bytes, data: str) -> None:
    encrypted = encrypt(data, password)
    storage.store(key, encrypted)
