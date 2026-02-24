from __future__ import annotations

import aiohttp
from aiohttp import CookieJar

from insta_wizard import InstagramClientLogger, TransportResponse, TransportSettings
from insta_wizard.common.transport.base import HttpTransport
from insta_wizard.common.transport.exceptions import TransportNetworkError, TransportTimeoutError
from insta_wizard.common.transport.models import HttpRequest


class LoggingClientRequest(aiohttp.ClientRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        session = kwargs.get("session")
        logger: InstagramClientLogger = getattr(session, "_wire_logger", None) if session else None
        if not logger:
            return

        headers_str = "\n".join(f"  {k}: {v}" for k, v in dict(self.headers).items())

        body_str = self.body.decode("utf-8", errors="replace")

        msg = (
            "Request\n"
            f"Method: {self.method}\n"
            f"URL: {self.url}\n"
            "Headers:\n"
            f"{headers_str}\n"
            "Body:\n"
            f"  {body_str if body_str else '<empty>'}\n"
        )

        logger.request("%s", msg)


class AioHttpTransport(HttpTransport):
    def __init__(
        self,
        *,
        settings: TransportSettings,
        logger: InstagramClientLogger,
        proxy_url: str | None = None,
        timeout: int | float | None = None,
        cookie_jar: CookieJar | None = None,
    ):
        super().__init__(settings=settings, logger=logger, proxy_url=proxy_url)

        self._session = aiohttp.ClientSession(
            request_class=LoggingClientRequest,
            timeout=aiohttp.ClientTimeout(total=timeout),
            cookie_jar=(cookie_jar if cookie_jar is not None else aiohttp.DummyCookieJar()),
        )
        self._session._wire_logger = logger

    async def set_proxy(self, proxy_url: str | None) -> None:
        self._proxy_url = proxy_url

    async def send(self, request: HttpRequest, follow_redirects: bool = True) -> TransportResponse:
        return await self._send_with_retries(request, self._send, follow_redirects=follow_redirects)

    async def _send(self, request: HttpRequest, follow_redirects: bool = True) -> TransportResponse:
        try:
            async with self._session.request(
                request.method,
                request.url,
                params=request.params,
                data=request.data,
                headers=request.headers,
                cookies=request.cookies,
                proxy=self._proxy_url,
                allow_redirects=follow_redirects,
            ) as resp:
                content = await resp.read()

                return TransportResponse(
                    status=resp.status,
                    headers=dict(resp.headers),
                    content=content,
                    url=str(resp.url),
                    http_version=f"HTTP/{resp.version.major}.{resp.version.minor}",
                )

        except TimeoutError as e:
            raise TransportTimeoutError("Request timeout") from e
        except aiohttp.ClientError as e:
            raise TransportNetworkError(f"aiohttp error: {e}") from e

    async def close(self) -> None:
        await self._session.close()
