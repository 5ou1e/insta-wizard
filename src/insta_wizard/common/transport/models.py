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


@dataclass
class TransportSettings:
    http_version: Literal["1"] = "1"

    max_network_wait_time: float = 30.0
    max_retries_on_network_errors: int = 0
    delay_before_retries_on_network_errors: float = 0.0
    change_proxy_after_all_failed_attempts: bool = False
    max_proxy_changes: int | None = None
    proxy_provider: ProxyProvider | None = None

    def __post_init__(self) -> None:
        if self.max_network_wait_time < 0:
            raise ValueError("max_network_wait_time must be >= 0")

        if self.max_retries_on_network_errors < 0:
            raise ValueError("max_retries_on_network_errors must be >= 0")

        if self.delay_before_retries_on_network_errors < 0:
            raise ValueError("delay_before_retries_on_network_errors must be >= 0")

        if self.change_proxy_after_all_failed_attempts and self.proxy_provider is None:
            raise ValueError("change_proxy_after_all_failed_attempts=True requires proxy_provider")
        if self.http_version not in ["1"]:
            raise ValueError("Unknown http_version provided")
