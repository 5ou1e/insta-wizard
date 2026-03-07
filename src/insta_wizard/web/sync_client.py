from __future__ import annotations

import asyncio
import threading

from insta_wizard.common.logger import InstagramClientLogger
from insta_wizard.common.models.proxy import ProxyInfo
from insta_wizard.common.transport.models import TransportSettings
from insta_wizard.web.client import WebClient
from insta_wizard.web.common.command import Command, R
from insta_wizard.web.models.device_info import BrowserDeviceInfo
from insta_wizard.web.models.local_data import WebClientLocalData


class SyncSection:
    def __init__(self, async_section, run_fn):
        self._s = async_section
        self._run = run_fn

    def __getattr__(self, name):
        attr = getattr(self._s, name)
        if asyncio.iscoroutinefunction(attr):

            def wrapper(*args, **kwargs):
                return self._run(attr(*args, **kwargs))

            return wrapper
        return attr


class SyncWebClient:
    """Synchronous wrapper around WebClient.

    Runs an async event loop in a background daemon thread.
    Use as a context manager or call .close() when done.
    """

    def __init__(
        self,
        device: BrowserDeviceInfo | None = None,
        local_data: WebClientLocalData | None = None,
        proxy: ProxyInfo | None = None,
        transport_settings: TransportSettings | None = None,
        logger: InstagramClientLogger | None = None,
    ):
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()

        self._async_client: WebClient = asyncio.run_coroutine_threadsafe(
            self._create_async_client(
                device=device,
                local_data=local_data,
                proxy=proxy,
                transport_settings=transport_settings,
                logger=logger,
            ),
            self._loop,
        ).result()

        self.state = self._async_client.state
        self.account = SyncSection(self._async_client.account, self._run)  # type: ignore[assignment]
        self.challenge = SyncSection(self._async_client.challenge, self._run)  # type: ignore[assignment]
        self.comments = SyncSection(self._async_client.comments, self._run)  # type: ignore[assignment]
        self.friendships = SyncSection(self._async_client.friendships, self._run)  # type: ignore[assignment]
        self.likes = SyncSection(self._async_client.likes, self._run)  # type: ignore[assignment]
        self.navigation = SyncSection(self._async_client.navigation, self._run)  # type: ignore[assignment]
        self.user = SyncSection(self._async_client.user, self._run)  # type: ignore[assignment]

    @staticmethod
    async def _create_async_client(**kwargs) -> WebClient:
        return WebClient(**kwargs)

    def _run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result()

    def execute(self, command: Command[R]) -> R:
        return self._run(self._async_client.execute(command))

    def close(self) -> None:
        self._run(self._async_client.close())
        self._loop.call_soon_threadsafe(self._loop.stop)  # type: ignore[arg-type]
        self._thread.join()

    def __enter__(self) -> SyncWebClient:
        return self

    def __exit__(self, *_) -> None:
        self.close()

    def set_proxy(self, proxy: ProxyInfo | None) -> None:
        self._run(self._async_client.set_proxy(proxy))

    def get_local_data(self) -> WebClientLocalData:
        return self._async_client.get_local_data()

    def get_cookies(self) -> dict:
        return self._async_client.get_cookies()

    def set_cookies(self, cookies: dict) -> None:
        self._async_client.set_cookies(cookies)

    def dump_state(self) -> dict:
        return self._async_client.dump_state()

    def load_state(self, state: dict) -> None:
        self._async_client.load_state(state)

    def initialize_state(self) -> None:
        """Navigate to home page and parse parameters required for the client to work"""
        self._run(self._async_client.initialize_state())

    def login(self, username: str, password: str) -> None:
        """Log in to account using username and password"""
        self._run(self._async_client.login(username=username, password=password))

    def logout(self) -> None:
        """Logout of account"""
        self._run(self._async_client.logout())
