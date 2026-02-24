import base64

import pytest


@pytest.fixture()
def rsa_public_key_b64() -> str:
    """Генерирует RSA 2048 публичный ключ в формате base64(DER) для тестов encrypt_v4."""
    from Cryptodome.PublicKey import RSA

    key = RSA.generate(2048)
    return base64.b64encode(key.publickey().export_key("DER")).decode()


@pytest.fixture()
def nacl_keypair():
    """
    Генерирует NaCl keypair.
    Возвращает (PrivateKey, pub_hex: str) — pub_hex в формате который принимает encrypt_v10.
    """
    from nacl.public import PrivateKey

    private = PrivateKey.generate()
    pub_hex = bytes(private.public_key).hex()
    return private, pub_hex
