import base64
import json

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def decrypt(text: str) -> dict:
    key = b'1234567890123456'
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    text = (text + "=" * (4 - len(text) % 4)).replace("-", "+").replace("_", "/")
    text = base64.b64decode(text)
    content = decryptor.update(text) + decryptor.finalize()
    return json.loads(content[:-content[-1]].decode())
