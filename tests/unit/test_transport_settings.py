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
        assert s.network_timeout == 30.0
        assert s.network_error_retry_limit == 0
        assert s.proxy_provider is None


class TestTransportSettingsValidation:
    def test_negative_wait_time_raises(self):
        with pytest.raises(ValueError, match="network_timeout"):
            TransportSettings(network_timeout=-1)

    def test_zero_wait_time_is_allowed(self):
        s = TransportSettings(network_timeout=0)
        assert s.network_timeout == 0

    def test_negative_retries_raises(self):
        with pytest.raises(ValueError, match="network_error_retry_limit"):
            TransportSettings(network_error_retry_limit=-1)

    def test_zero_retries_is_allowed(self):
        s = TransportSettings(network_error_retry_limit=0)
        assert s.network_error_retry_limit == 0

    def test_negative_delay_raises(self):
        with pytest.raises(ValueError, match="network_error_retry_delay"):
            TransportSettings(network_error_retry_delay=-0.1)

    def test_zero_delay_is_allowed(self):
        s = TransportSettings(network_error_retry_delay=0.0)
        assert s.network_error_retry_delay == 0.0

    def test_change_proxy_without_provider_raises(self):
        with pytest.raises(ValueError, match="proxy_provider"):
            TransportSettings(change_proxies=True)

    def test_change_proxy_with_provider_is_valid(self):
        provider = AsyncMock()
        s = TransportSettings(
            change_proxies=True,
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
