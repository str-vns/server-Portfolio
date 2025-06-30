import sys
import base64
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
from decouple import config as env_config

def EncryptToken(token_secret):
    aes_key = get_random_bytes(32)
    hmac_key = get_random_bytes(32)
    nonce = get_random_bytes(8)

    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)
    cipherText = cipher.encrypt(token_secret)
    hmac = HMAC.new(hmac_key, digestmod=SHA256)
    tag = hmac.update(cipher.nonce + cipherText).digest()

    with open("encrypted.bin", "wb") as f:
        f.write(aes_key)
        f.write(hmac_key)
        f.write(cipher.nonce)
        f.write(cipherText)
        f.write(tag)
        
        tag_b64 = base64.b64encode(tag).decode("utf-8")
    return {"tag": tag_b64}


def DecryptToken(tags):
    if isinstance(tags, str):
        tags = base64.b64decode(tags)
    with open("encrypted.bin", "rb") as f:
        aes_key = f.read(32)
        hmac_key = f.read(32)
        nonce = f.read(8)
        file_content = f.read()
        cipherText = file_content[:-32]

    try:
        hmac = HMAC.new(hmac_key, digestmod=SHA256)
        hmac.update(nonce + cipherText).verify(tags)

    except ValueError:
        print("The message was Modified")
        return False

    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)
    decrypted = cipher.decrypt(cipherText)
    if decrypted == env_config("TOKEN_SECRET"):
       return True
