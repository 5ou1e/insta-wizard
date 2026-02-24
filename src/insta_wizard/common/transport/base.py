from __future__ import annotations

import asyncio
import ssl
from collections.abc import Awaitable, Callable

from insta_wizard.common.logger import InstagramClientLogger
from insta_wizard.common.transport.exceptions import (
    TransportError,
    TransportNetworkError,
    TransportTimeoutError,
)
from insta_wizard.common.transport.models import (
    HttpRequest,
    TransportResponse,
    TransportSettings,
)

SSL_CONTEXT = ssl.create_default_context()


class HttpTransport:
    def __init__(
        self,
        *,
        settings: TransportSettings,
        logger: InstagramClientLogger,
        proxy_url: str | None = None,
    ) -> None:
        self._settings = settings
        self._logger = logger
        self._proxy_url = proxy_url
        self._send_lock = asyncio.Lock()

    async def send(self, request: HttpRequest, follow_redirects: bool = True) -> TransportResponse:
        raise NotImplementedError

    async def set_proxy(self, proxy_url: str | None) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError

    async def _send_with_retries(
        self,
        request: HttpRequest,
        send_once: Callable[[HttpRequest], Awaitable[TransportResponse]],
        follow_redirects: bool = True,
    ) -> TransportResponse:
        s = self._settings

        if s.max_retries_on_network_errors <= 0 and not s.change_proxy_after_all_failed_attempts:
            return await send_once(request, follow_redirects=follow_redirects)

        async with self._send_lock:
            proxy_changes_done = 0
            last_exc: TransportError | None = None

            while True:
                max_attempts = 1 + max(0, s.max_retries_on_network_errors)

                for attempt_idx in range(max_attempts):
                    try:
                        return await send_once(request, follow_redirects=follow_redirects)

                    except (TransportTimeoutError, TransportNetworkError) as e:
                        self._logger.info("Ошибка соединения: %s", e)
                        last_exc = e

                        is_last_attempt = attempt_idx == max_attempts - 1
                        if not is_last_attempt:
                            if s.delay_before_retries_on_network_errors > 0:
                                await asyncio.sleep(s.delay_before_retries_on_network_errors)
                            continue

                        break

                assert last_exc is not None

                if not s.change_proxy_after_all_failed_attempts:
                    raise last_exc

                if s.max_proxy_changes is not None and proxy_changes_done >= s.max_proxy_changes:
                    raise last_exc

                provider = s.proxy_provider

                new_proxy = await provider.provide_new()
                await self.set_proxy(new_proxy.url)

                proxy_changes_done += 1

                if s.delay_before_retries_on_network_errors > 0:
                    await asyncio.sleep(s.delay_before_retries_on_network_errors)
