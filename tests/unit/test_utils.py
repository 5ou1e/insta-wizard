"""
Тесты для insta_wizard.common.utils.
Внешних сервисов не требует.
"""

import base64
import uuid

import orjson
import pytest

from insta_wizard.common.generators import generate_android_id_from_guid
from insta_wizard.common.utils import (
    auth_data_from_authorization_header,
    locale_code_to_bcp47,
    normalize_locale_code,
)


class TestNormalizeLocaleCode:
    @pytest.mark.parametrize(
        "input_code, expected",
        [
            ("ru_RU", "ru_RU"),
            ("en_us", "en_US"),
            ("RU_ru", "ru_RU"),
            ("en-US", "en_US"),
            ("en-us", "en_US"),
            ("EN-US", "en_US"),
        ],
    )
    def test_normalizes_correctly(self, input_code, expected):
        assert normalize_locale_code(input_code) == expected

    def test_single_part_unchanged(self):
        # Нет разделителя — возвращается как есть
        assert normalize_locale_code("en") == "en"


class TestLocaleCodeToBcp47:
    @pytest.mark.parametrize(
        "input_code, expected",
        [
            ("ru_RU", "ru-RU"),
            ("en-us", "en-US"),
            ("en-US", "en-US"),
            ("EN_US", "en-US"),
        ],
    )
    def test_converts_correctly(self, input_code, expected):
        assert locale_code_to_bcp47(input_code) == expected

    def test_single_part_lowercased(self):
        assert locale_code_to_bcp47("EN") == "en"

    def test_result_is_cached(self):
        # lru_cache — повторный вызов не должен менять результат
        r1 = locale_code_to_bcp47("ru_RU")
        r2 = locale_code_to_bcp47("ru_RU")
        assert r1 == r2


class TestGenerateAndroidIdFromGuid:
    def test_format_starts_with_android_prefix(self):
        result = generate_android_id_from_guid(uuid.uuid4())
        assert result.startswith("android-")

    def test_length_is_correct(self):
        # "android-" + 16 hex chars
        result = generate_android_id_from_guid(uuid.uuid4())
        assert len(result) == len("android-") + 16

    def test_deterministic_for_same_guid(self):
        guid = "3dfd6b8a-1e34-4d61-abca-aa268e405550"
        assert generate_android_id_from_guid(guid) == generate_android_id_from_guid(guid)

    def test_known_value(self):
        # Зафиксированный результат — если алгоритм изменится, тест упадёт
        guid = "3dfd6b8a-1e34-4d61-abca-aa268e405550"
        result = generate_android_id_from_guid(guid)
        # Вычислено: md5("3dfd6b8a-1e34-4d61-abca-aa268e405550")[:16]
        import hashlib

        expected = "android-" + hashlib.md5(str(guid).encode()).hexdigest()[:16]
        assert result == expected

    def test_different_guids_give_different_ids(self):
        a = generate_android_id_from_guid(uuid.uuid4())
        b = generate_android_id_from_guid(uuid.uuid4())
        assert a != b

    def test_accepts_uuid_object(self):
        guid = uuid.UUID("3dfd6b8a-1e34-4d61-abca-aa268e405550")
        result = generate_android_id_from_guid(guid)
        assert result.startswith("android-")


class TestAuthDataFromAuthorizationHeader:
    def test_parses_base64_json_from_last_colon_segment(self):
        data = {"ds_user_id": "123456", "sessionid": "abc"}
        b64 = base64.b64encode(orjson.dumps(data)).decode()
        header = f"Basic IGUserId:{b64}"
        result = auth_data_from_authorization_header(header)
        assert result == data

    def test_returns_empty_dict_when_last_segment_empty(self):
        # "Bearer:" → split даёт ["Bearer", ""] → b64part = "" → falsy
        result = auth_data_from_authorization_header("Bearer:")
        assert result == {}

    def test_nested_json_preserved(self):
        data = {"user": {"id": 1}, "tokens": ["a", "b"]}
        b64 = base64.b64encode(orjson.dumps(data)).decode()
        header = f"prefix:{b64}"
        assert auth_data_from_authorization_header(header) == data
