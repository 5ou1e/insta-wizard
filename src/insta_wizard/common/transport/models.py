from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Literal

from yarl import URL

from insta_wizard.common.interfaces import ProxyProvider

HttpMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]


@dataclass(kw_only=True, slots=True)
class HttpRequest:
    method: HttpMethod
    url: str | URL
    headers: dict[str, str] = field(default_factory=dict)
    data: Any | None = None
    params: dict[str, str] | None = None
    cookies: dict | None = None


@dataclass(frozen=True, slots=True)
class TransportResponse:
    status: int
    headers: dict[str, str]
    content: bytes
    url: str
    http_version: str | None = None


@dataclass(kw_only=True, slots=True)
class ResponseInfo:
    status: int
    headers: Mapping[str, str]
    json: Any = None
    text: str | None = None

    @property
    def response_string(self):
        return str(self.json) if self.json else self.text


@dataclass
class TransportSettings:
    engine: Literal["aiohttp"] = "aiohttp"
    http_version: Literal["1", "2"] = "1"

    network_timeout: float = 30.0
    network_error_retry_limit: int = 0
    network_error_retry_delay: float = 0.0
    change_proxies: bool = False
    proxy_change_limit: int | None = None
    proxy_provider: ProxyProvider | None = None

    def __post_init__(self) -> None:
        if self.network_timeout < 0:
            raise ValueError("network_timeout must be >= 0")

        if self.network_error_retry_limit < 0:
            raise ValueError("network_error_retry_limit must be >= 0")

        if self.network_error_retry_delay < 0:
            raise ValueError("network_error_retry_delay must be >= 0")

        if self.change_proxies and self.proxy_provider is None:
            raise ValueError("change_proxies=True requires proxy_provider")

        if self.http_version not in ["1", "2"]:
            raise ValueError("Unknown http_version provided")
