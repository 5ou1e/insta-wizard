import re
from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar

PROXY_PATTERN = re.compile(
    r"^\s*"
    r"(?:(?P<protocol>[a-zA-Z][a-zA-Z0-9+.-]*)://)?"
    r"(?:(?P<u1>[^:@\s]+)(?::(?P<p1>[^@\s]*))?@)?"
    r"(?P<host>\[[^\]]+\]|[^:\s]+)"
    r":(?P<port>\d{1,5})"
    r"(?::(?P<u2>[^:\s]+):(?P<p2>[^\s]+))?"
    r"\s*$"
)


class ProxyProtocol(StrEnum):
    HTTP = "http"


@dataclass(kw_only=True)
class ProxyInfo:
    """Read-model для прокси"""

    protocol: "ProxyProtocol" = ProxyProtocol.HTTP
    host: str
    port: int
    username: str | None = None
    password: str | None = None

    _pattern: ClassVar[re.Pattern] = PROXY_PATTERN

    @property
    def url(self) -> str:
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"

    @classmethod
    def from_string(
        cls,
        string: str,
    ) -> "ProxyInfo":
        """
        Поддерживаемые форматы:
         - [protocol://][user:pass@]host:port[:user:pass]

        Примеры:
          - 1.2.3.4:8080
          - http://1.2.3.4:8080
          - user:pass@1.2.3.4:8080
          - http://user:pass@1.2.3.4:8080
          - 1.2.3.4:8080:user:pass
          - http://1.2.3.4:8080:user:pass
        """
        if string is None:
            raise ValueError(f"Некорректный формат Proxy: {string}")

        s = string.strip()
        if not s:
            raise ValueError(f"Некорректный формат Proxy: {string}")

        m = cls._pattern.match(s)
        if not m:
            raise ValueError(f"Некорректный формат Proxy: {string}")

        gd = m.groupdict()

        host = gd["host"]

        if host.startswith("[") and host.endswith("]"):
            host = host[1:-1]

        try:
            port = int(gd["port"])
        except (TypeError, ValueError):
            raise ValueError(f"Некорректный формат Proxy : {string}")

        if not (1 <= port <= 65535):
            raise ValueError(f"Некорректный формат Proxy : {string}")

        username = gd.get("u1") or gd.get("u2")
        password = gd.get("p1") or gd.get("p2")

        protocol_raw = (gd.get("protocol") or "http").lower()
        try:
            protocol = ProxyProtocol(protocol_raw)
        except Exception:
            protocol = ProxyProtocol.HTTP

        return cls(
            protocol=protocol,
            host=host,
            port=port,
            username=username or None,
            password=password or None,
        )


@dataclass(kw_only=True, slots=True)
class EncryptionInfo:
    publickeyid: int
    publickey: str
    version: int
