import base64
import binascii
import struct
import time
from typing import Literal

# pip install pycryptodomex
from Cryptodome.Cipher import AES, PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes

# pip install PyNaCl
from nacl.public import PublicKey, SealedBox

from insta_wizard.common.models import EncryptionInfo


class PasswordEncrypter:
    @classmethod
    def encrypt(
        cls,
        password: str,
        encryption_info: EncryptionInfo,
        prefix: Literal["PWD_INSTAGRAM", "PWD_INSTAGRAM_BROWSER"] = "PWD_INSTAGRAM",
        timestamp: str | None = None,
    ):
        if encryption_info.version == 10:
            enc_password = PasswordEncrypter.encrypt_v10(
                password,
                publickeyid=encryption_info.publickeyid,
                publickey=encryption_info.publickey,
                prefix=prefix,
                timestamp=timestamp,
            )
            return enc_password
        else:
            raise ValueError(f"Unsupported EncryptionInfo version: {encryption_info.version}")

    @classmethod
    def encrypt_v4(
        cls,
        password,
        publickeyid: int,
        publickey: str,
        prefix: Literal["PWD_INSTAGRAM", "PWD_INSTAGRAM_BROWSER"] = "PWD_INSTAGRAM",
        timestamp: str | None = None,
    ):
        if not timestamp:
            timestamp = str(int(time.time()))

        session_key = get_random_bytes(32)
        iv = get_random_bytes(12)
        decoded_publickey = base64.b64decode(publickey.encode())
        recipient_key = RSA.import_key(decoded_publickey)
        cipher_rsa = PKCS1_v1_5.new(recipient_key)
        rsa_encrypted = cipher_rsa.encrypt(session_key)
        cipher_aes = AES.new(session_key, AES.MODE_GCM, iv)
        cipher_aes.update(timestamp.encode())
        aes_encrypted, tag = cipher_aes.encrypt_and_digest(password.encode("utf8"))
        size_buffer = len(rsa_encrypted).to_bytes(2, byteorder="little")
        payload = base64.b64encode(
            b"".join(
                [
                    b"\x01",
                    int(publickeyid).to_bytes(1, byteorder="big"),
                    iv,
                    size_buffer,
                    rsa_encrypted,
                    tag,
                    aes_encrypted,
                ]
            )
        )
        return f"#{prefix}:4:{timestamp}:{payload.decode()}"

    @classmethod
    def encrypt_v10(
        cls,
        password: str,
        publickeyid: int,
        publickey: str,
        prefix: Literal["PWD_INSTAGRAM", "PWD_INSTAGRAM_BROWSER"] = "PWD_INSTAGRAM",
        timestamp: str | None = None,
    ):
        if not timestamp:
            timestamp = str(int(time.time()))

        key = get_random_bytes(32)
        iv = bytes([0] * 12)

        aes = AES.new(key, AES.MODE_GCM, nonce=iv, mac_len=16)
        aes.update(str(timestamp).encode("utf-8"))
        encrypted_password, cipher_tag = aes.encrypt_and_digest(password.encode("utf-8"))

        pub_key_bytes = binascii.unhexlify(publickey)
        seal_box = SealedBox(PublicKey(pub_key_bytes))
        encrypted_key = seal_box.encrypt(key)

        encrypted = bytes(
            [
                1,
                publickeyid,
                *list(struct.pack("<h", len(encrypted_key))),
                *list(encrypted_key),
                *list(cipher_tag),
                *list(encrypted_password),
            ]
        )
        encrypted = base64.b64encode(encrypted).decode("utf-8")

        return f"#{prefix}:10:{timestamp}:{encrypted}"

    @classmethod
    def encrypt_v0(
        cls,
        password: str,
        prefix: Literal["PWD_INSTAGRAM", "PWD_INSTAGRAM_BROWSER"] = "PWD_INSTAGRAM",
    ) -> str:
        return f"#{prefix}:0:{int(time.time())}:{password}"
