"""
Тесты для insta_wizard.common.generators.
Внешних сервисов не требует.
"""

import pytest

from insta_wizard.common.generators import generate_jazoest, utc_offset_from_timezone


class TestGenerateJazoest:
    def test_result_starts_with_2(self):
        assert generate_jazoest("abc").startswith("2")

    def test_known_value(self):
        # ord('a')=97, ord('b')=98, ord('c')=99 → sum=294 → "2294"
        assert generate_jazoest("abc") == "2294"

    def test_empty_string(self):
        assert generate_jazoest("") == "20"

    def test_single_char(self):
        # ord('A') = 65 → "265"
        assert generate_jazoest("A") == "265"

    def test_deterministic(self):
        assert generate_jazoest("hello") == generate_jazoest("hello")


class TestUtcOffsetFromTimezone:
    def test_utc_returns_zero(self):
        assert utc_offset_from_timezone("UTC") == 0

    def test_moscow_returns_utc_plus_3(self):
        # Москва: UTC+3, без перехода на летнее время
        assert utc_offset_from_timezone("Europe/Moscow") == 3 * 3600

    def test_london_returns_zero_or_plus_1(self):
        # Лондон: зимой UTC+0, летом BST (UTC+1)
        offset = utc_offset_from_timezone("Europe/London")
        assert offset in (0, 3600)

    def test_new_york_returns_negative(self):
        # Нью-Йорк: EST (UTC-5) или EDT (UTC-4)
        offset = utc_offset_from_timezone("America/New_York")
        assert offset in (-5 * 3600, -4 * 3600)

    def test_invalid_timezone_raises(self):
        with pytest.raises(Exception):
            utc_offset_from_timezone("Not/A/Timezone")
