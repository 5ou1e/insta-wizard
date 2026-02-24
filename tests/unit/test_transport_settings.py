"""
Тесты для TransportSettings.__post_init__ валидации.
Внешних сервисов не требует.
"""

from unittest.mock import AsyncMock

import pytest

from insta_wizard.common.transport.models import TransportSettings


class TestTransportSettingsDefaults:
    def test_default_construction_succeeds(self):
        s = TransportSettings()
        assert s.engine == "aiohttp"
        assert s.max_network_wait_time == 30.0
        assert s.max_retries_on_network_errors == 0
        assert s.proxy_provider is None


class TestTransportSettingsValidation:
    def test_negative_wait_time_raises(self):
        with pytest.raises(ValueError, match="max_network_wait_time"):
            TransportSettings(max_network_wait_time=-1)

    def test_zero_wait_time_is_allowed(self):
        s = TransportSettings(max_network_wait_time=0)
        assert s.max_network_wait_time == 0

    def test_negative_retries_raises(self):
        with pytest.raises(ValueError, match="max_retries_on_network_errors"):
            TransportSettings(max_retries_on_network_errors=-1)

    def test_zero_retries_is_allowed(self):
        s = TransportSettings(max_retries_on_network_errors=0)
        assert s.max_retries_on_network_errors == 0

    def test_negative_delay_raises(self):
        with pytest.raises(ValueError, match="delay_before_retries_on_network_errors"):
            TransportSettings(delay_before_retries_on_network_errors=-0.1)

    def test_zero_delay_is_allowed(self):
        s = TransportSettings(delay_before_retries_on_network_errors=0.0)
        assert s.delay_before_retries_on_network_errors == 0.0

    def test_change_proxy_without_provider_raises(self):
        with pytest.raises(ValueError, match="proxy_provider"):
            TransportSettings(change_proxy_after_all_failed_attempts=True)

    def test_change_proxy_with_provider_is_valid(self):
        provider = AsyncMock()
        s = TransportSettings(
            change_proxy_after_all_failed_attempts=True,
            proxy_provider=provider,
        )
        assert s.proxy_provider is provider

    def test_invalid_http_version_raises(self):
        with pytest.raises(ValueError, match="http_version"):
            TransportSettings(http_version="3")  # type: ignore[arg-type]

    @pytest.mark.parametrize("version", ["1", "2"])
    def test_valid_http_versions(self, version):
        s = TransportSettings(http_version=version)  # type: ignore[arg-type]
        assert s.http_version == version
