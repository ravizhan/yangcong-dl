import json
from Crypto.Cipher import AES
import base64


def dec(text:str):
    key = b"1234567890123456"
    cipher = AES.new(key, AES.MODE_ECB)
    content = cipher.decrypt(base64.urlsafe_b64decode(text+"="*(len(text) % 4)))
    content = content[:-content[-1]].decode()
    return json.loads(content)

