"""
Тесты для PasswordEncrypter.
- v0: полностью тестируется (нет крипто, пароль в открытом виде)
- v4: тестируется структура вывода (RSA + AES-GCM, ключ генерируется в фикстуре)
- v10: тестируется структура + roundtrip расшифровки (NaCl + AES-GCM)
Внешних сервисов не требует.
"""

import base64
import re
import struct

import pytest

from insta_wizard.common.models.other import EncryptionInfo
from insta_wizard.common.password_encrypter import PasswordEncrypter

# Паттерны ожидаемого формата вывода
_PAT_V0 = re.compile(r"^#PWD_INSTAGRAM:0:\d+:.+$")
_PAT_V4 = re.compile(r"^#PWD_INSTAGRAM:4:\d+:.+$")
_PAT_V10 = re.compile(r"^#PWD_INSTAGRAM:10:\d+:.+$")
_PAT_BROWSER = re.compile(r"^#PWD_INSTAGRAM_BROWSER:")


class TestEncryptV0:
    """encrypt_v0 — пароль не шифруется, просто оборачивается в формат."""

    def test_output_matches_format(self):
        result = PasswordEncrypter.encrypt_v0("mypassword")
        assert _PAT_V0.match(result), f"Unexpected format: {result}"

    def test_password_in_plaintext_at_end(self):
        result = PasswordEncrypter.encrypt_v0("mypassword")
        assert result.endswith(":mypassword")

    def test_timestamp_is_numeric(self):
        result = PasswordEncrypter.encrypt_v0("x")
        parts = result.split(":")
        # формат: #PREFIX:0:TIMESTAMP:PASSWORD
        assert parts[2].isdigit()

    def test_browser_prefix(self):
        result = PasswordEncrypter.encrypt_v0("x", prefix="PWD_INSTAGRAM_BROWSER")
        assert _PAT_BROWSER.match(result)
        assert ":0:" in result

    def test_empty_password(self):
        result = PasswordEncrypter.encrypt_v0("")
        assert result.endswith(":")


class TestEncryptV4:
    """encrypt_v4 — RSA + AES-GCM. Проверяем структуру вывода."""

    def test_output_matches_format(self, rsa_public_key_b64):
        result = PasswordEncrypter.encrypt_v4(
            "testpassword",
            publickeyid=178,
            publickey=rsa_public_key_b64,
            timestamp="1700000000",
        )
        assert _PAT_V4.match(result), f"Unexpected format: {result}"

    def test_fixed_timestamp_appears_in_output(self, rsa_public_key_b64):
        result = PasswordEncrypter.encrypt_v4(
            "testpassword",
            publickeyid=178,
            publickey=rsa_public_key_b64,
            timestamp="1700000000",
        )
        parts = result.split(":")
        assert parts[2] == "1700000000"

    def test_payload_is_valid_base64(self, rsa_public_key_b64):
        result = PasswordEncrypter.encrypt_v4(
            "pass", publickeyid=1, publickey=rsa_public_key_b64, timestamp="1700000000"
        )
        payload = result.split(":")[-1]
        # не должно бросить исключение
        base64.b64decode(payload)

    def test_non_deterministic_output(self, rsa_public_key_b64):
        """Каждый вызов должен давать разный шифртекст (случайный session key)."""
        kwargs = dict(publickeyid=1, publickey=rsa_public_key_b64, timestamp="1700000000")
        r1 = PasswordEncrypter.encrypt_v4("pass", **kwargs)
        r2 = PasswordEncrypter.encrypt_v4("pass", **kwargs)
        assert r1 != r2

    def test_browser_prefix(self, rsa_public_key_b64):
        result = PasswordEncrypter.encrypt_v4(
            "pass",
            publickeyid=1,
            publickey=rsa_public_key_b64,
            prefix="PWD_INSTAGRAM_BROWSER",
            timestamp="1700000000",
        )
        assert _PAT_BROWSER.match(result)


class TestEncryptV10:
    """encrypt_v10 — NaCl SealedBox + AES-GCM."""

    def test_output_matches_format(self, nacl_keypair):
        _, pub_hex = nacl_keypair
        result = PasswordEncrypter.encrypt_v10(
            "testpassword", publickeyid=5, publickey=pub_hex, timestamp="1700000000"
        )
        assert _PAT_V10.match(result), f"Unexpected format: {result}"

    def test_fixed_timestamp_in_output(self, nacl_keypair):
        _, pub_hex = nacl_keypair
        result = PasswordEncrypter.encrypt_v10(
            "pass", publickeyid=5, publickey=pub_hex, timestamp="1700000000"
        )
        parts = result.split(":")
        assert parts[2] == "1700000000"

    def test_payload_is_valid_base64(self, nacl_keypair):
        _, pub_hex = nacl_keypair
        result = PasswordEncrypter.encrypt_v10(
            "pass", publickeyid=5, publickey=pub_hex, timestamp="1700000000"
        )
        payload = result.split(":")[-1]
        base64.b64decode(payload)

    def test_non_deterministic_output(self, nacl_keypair):
        """SealedBox использует эфемерный keypair — шифртекст уникален каждый раз."""
        _, pub_hex = nacl_keypair
        kwargs = dict(publickeyid=5, publickey=pub_hex, timestamp="1700000000")
        r1 = PasswordEncrypter.encrypt_v10("pass", **kwargs)
        r2 = PasswordEncrypter.encrypt_v10("pass", **kwargs)
        assert r1 != r2

    def test_browser_prefix(self, nacl_keypair):
        _, pub_hex = nacl_keypair
        result = PasswordEncrypter.encrypt_v10(
            "pass",
            publickeyid=5,
            publickey=pub_hex,
            prefix="PWD_INSTAGRAM_BROWSER",
            timestamp="1700000000",
        )
        assert _PAT_BROWSER.match(result)

    def test_decrypt_roundtrip(self, nacl_keypair):
        """Шифруем → расшифровываем вручную → сравниваем с оригиналом."""
        from Cryptodome.Cipher import AES
        from nacl.public import SealedBox

        private_key, pub_hex = nacl_keypair
        password = "supersecret123!@#"
        timestamp = "1700000000"

        result = PasswordEncrypter.encrypt_v10(
            password, publickeyid=5, publickey=pub_hex, timestamp=timestamp
        )

        payload = base64.b64decode(result.split(":")[-1])

        # Структура: [1 byte version][1 byte key_id][2 bytes LE key_len][encrypted_key][16 bytes tag][encrypted_password]
        key_len = struct.unpack("<h", payload[2:4])[0]
        encrypted_key = payload[4 : 4 + key_len]
        cipher_tag = payload[4 + key_len : 4 + key_len + 16]
        encrypted_password = payload[4 + key_len + 16 :]

        aes_key = SealedBox(private_key).decrypt(encrypted_key)

        iv = bytes(12)
        aes = AES.new(aes_key, AES.MODE_GCM, nonce=iv, mac_len=16)
        aes.update(timestamp.encode("utf-8"))
        decrypted = aes.decrypt_and_verify(encrypted_password, cipher_tag)

        assert decrypted.decode("utf-8") == password


class TestEncryptDispatch:
    """Тесты для публичного метода encrypt() — диспетчер по версии."""

    def test_version_10_dispatches_to_encrypt_v10(self, nacl_keypair):
        _, pub_hex = nacl_keypair
        info = EncryptionInfo(publickeyid=5, publickey=pub_hex, version=10)
        result = PasswordEncrypter.encrypt("mypassword", info)
        assert _PAT_V10.match(result)

    def test_unsupported_version_raises_value_error(self):
        info = EncryptionInfo(publickeyid=1, publickey="key", version=99)
        with pytest.raises(ValueError, match="Unsupported"):
            PasswordEncrypter.encrypt("password", info)
