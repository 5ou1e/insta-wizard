"""
Тесты для ProxyInfo.from_string() — все 6 поддерживаемых форматов + edge cases.
Внешних сервисов не требует.
"""

import pytest

from insta_wizard.common.models import ProxyInfo, ProxyProtocol


class TestProxyInfoParsingFormats:
    """Все 6 задокументированных форматов."""

    def test_host_port(self):
        proxy = ProxyInfo.from_string("1.2.3.4:8080")
        assert proxy.host == "1.2.3.4"
        assert proxy.port == 8080
        assert proxy.username is None
        assert proxy.password is None
        assert proxy.protocol == ProxyProtocol.HTTP

    def test_protocol_host_port(self):
        proxy = ProxyInfo.from_string("http://1.2.3.4:8080")
        assert proxy.host == "1.2.3.4"
        assert proxy.port == 8080
        assert proxy.protocol == ProxyProtocol.HTTP

    def test_user_pass_at_host_port(self):
        proxy = ProxyInfo.from_string("user:pass@1.2.3.4:8080")
        assert proxy.host == "1.2.3.4"
        assert proxy.port == 8080
        assert proxy.username == "user"
        assert proxy.password == "pass"

    def test_protocol_user_pass_at_host_port(self):
        proxy = ProxyInfo.from_string("http://user:pass@1.2.3.4:8080")
        assert proxy.host == "1.2.3.4"
        assert proxy.port == 8080
        assert proxy.username == "user"
        assert proxy.password == "pass"

    def test_host_port_colon_user_pass(self):
        proxy = ProxyInfo.from_string("1.2.3.4:8080:user:pass")
        assert proxy.host == "1.2.3.4"
        assert proxy.port == 8080
        assert proxy.username == "user"
        assert proxy.password == "pass"

    def test_protocol_host_port_colon_user_pass(self):
        proxy = ProxyInfo.from_string("http://1.2.3.4:8080:user:pass")
        assert proxy.host == "1.2.3.4"
        assert proxy.port == 8080
        assert proxy.username == "user"
        assert proxy.password == "pass"


class TestProxyInfoParsingEdgeCases:
    def test_leading_trailing_whitespace_stripped(self):
        proxy = ProxyInfo.from_string("  1.2.3.4:8080  ")
        assert proxy.host == "1.2.3.4"
        assert proxy.port == 8080

    def test_port_boundary_min(self):
        proxy = ProxyInfo.from_string("1.2.3.4:1")
        assert proxy.port == 1

    def test_port_boundary_max(self):
        proxy = ProxyInfo.from_string("1.2.3.4:65535")
        assert proxy.port == 65535

    def test_domain_host(self):
        proxy = ProxyInfo.from_string("proxy.example.com:3128")
        assert proxy.host == "proxy.example.com"
        assert proxy.port == 3128

    def test_ipv6_host_brackets_stripped(self):
        proxy = ProxyInfo.from_string("[::1]:8080")
        assert proxy.host == "::1"
        assert proxy.port == 8080

    def test_unknown_protocol_falls_back_to_http(self):
        # Неизвестный протокол → HTTP по умолчанию (такое поведение в коде)
        proxy = ProxyInfo.from_string("socks5://1.2.3.4:1080")
        assert proxy.protocol == ProxyProtocol.HTTP
        assert proxy.host == "1.2.3.4"
        assert proxy.port == 1080

    def test_credentials_with_special_chars_in_password(self):
        proxy = ProxyInfo.from_string("user:p%40ss@1.2.3.4:8080")
        assert proxy.username == "user"
        assert proxy.password == "p%40ss"


class TestProxyInfoParsingErrors:
    @pytest.mark.parametrize(
        "bad_input",
        [
            "",  # пустая строка
            "   ",  # только пробелы
            "1.2.3.4",  # нет порта
            "1.2.3.4:0",  # порт вне диапазона (0)
            "1.2.3.4:65536",  # порт вне диапазона (> 65535)
        ],
    )
    def test_invalid_raises_value_error(self, bad_input):
        with pytest.raises(ValueError):
            ProxyInfo.from_string(bad_input)

    def test_none_raises_value_error(self):
        with pytest.raises(ValueError):
            ProxyInfo.from_string(None)  # type: ignore[arg-type]


class TestProxyInfoUrl:
    def test_url_without_credentials(self):
        proxy = ProxyInfo(host="1.2.3.4", port=8080)
        assert proxy.url == "http://1.2.3.4:8080"

    def test_url_with_credentials(self):
        proxy = ProxyInfo(host="1.2.3.4", port=8080, username="user", password="pass")
        assert proxy.url == "http://user:pass@1.2.3.4:8080"

    def test_url_username_only_no_auth_in_url(self):
        # username без password → auth не включается в URL
        proxy = ProxyInfo(host="1.2.3.4", port=8080, username="user", password=None)
        assert "@" not in proxy.url

    def test_url_roundtrip(self):
        # from_string → url → from_string должен давать те же данные
        original = "http://user:pass@1.2.3.4:8080"
        proxy = ProxyInfo.from_string(original)
        reparsed = ProxyInfo.from_string(proxy.url)
        assert reparsed.host == proxy.host
        assert reparsed.port == proxy.port
        assert reparsed.username == proxy.username
        assert reparsed.password == proxy.password
