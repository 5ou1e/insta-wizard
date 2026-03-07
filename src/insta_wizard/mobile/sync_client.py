from __future__ import annotations

import asyncio
import threading

from insta_wizard.common.logger import InstagramClientLogger
from insta_wizard.common.models.proxy import ProxyInfo
from insta_wizard.common.transport.models import TransportSettings
from insta_wizard.mobile.client import MobileClient
from insta_wizard.mobile.common.command import Command, R
from insta_wizard.mobile.models.android_device_info import AndroidDeviceInfo
from insta_wizard.mobile.models.local_data import MobileClientLocalData
from insta_wizard.mobile.models.version import InstagramAppVersion


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


class SyncMobileClient:
    """Synchronous wrapper around async MobileClient"""

    def __init__(
        self,
        device: AndroidDeviceInfo | None = None,
        version: InstagramAppVersion = InstagramAppVersion.V374,
        local_data: MobileClientLocalData | None = None,
        proxy: ProxyInfo | None = None,
        transport_settings: TransportSettings | None = None,
        logger: InstagramClientLogger | None = None,
    ):
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()

        self._async_client: MobileClient = asyncio.run_coroutine_threadsafe(
            self._create_async_client(
                device=device,
                version=version,
                local_data=local_data,
                proxy=proxy,
                transport_settings=transport_settings,
                logger=logger,
            ),
            self._loop,
        ).result()

        self.state = self._async_client.state
        self.account = SyncSection(self._async_client.account, self._run)  # type: ignore[assignment]
        self.users = SyncSection(self._async_client.users, self._run)  # type: ignore[assignment]
        self.friendships = SyncSection(self._async_client.friendships, self._run)  # type: ignore[assignment]
        self.feed = SyncSection(self._async_client.feed, self._run)  # type: ignore[assignment]
        self.direct = SyncSection(self._async_client.direct, self._run)  # type: ignore[assignment]
        self.media = SyncSection(self._async_client.media, self._run)  # type: ignore[assignment]
        self.notifications = SyncSection(self._async_client.notifications, self._run)  # type: ignore[assignment]
        self.news = SyncSection(self._async_client.news, self._run)  # type: ignore[assignment]
        self.live = SyncSection(self._async_client.live, self._run)  # type: ignore[assignment]
        self.clips = SyncSection(self._async_client.clips, self._run)  # type: ignore[assignment]
        self.challenge = SyncSection(self._async_client.challenge, self._run)  # type: ignore[assignment]
        self.registration = SyncSection(self._async_client.registration, self._run)  # type: ignore[assignment]

    @staticmethod
    async def _create_async_client(**kwargs) -> MobileClient:
        return MobileClient(**kwargs)

    def _run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result()

    def execute(self, command: Command[R]) -> R:
        return self._run(self._async_client.execute(command))

    def close(self) -> None:
        self._run(self._async_client.close())
        self._loop.call_soon_threadsafe(self._loop.stop)  # type: ignore[arg-type]
        self._thread.join()

    def __enter__(self) -> SyncMobileClient:
        return self

    def __exit__(self, *_) -> None:
        self.close()

    def set_proxy(self, proxy: ProxyInfo | None) -> None:
        self._run(self._async_client.set_proxy(proxy))

    def get_local_data(self) -> MobileClientLocalData:
        return self._async_client.get_local_data()

    def dump_state(self) -> dict:
        return self._async_client.dump_state()

    def load_state(self, state: dict) -> None:
        self._async_client.load_state(state)

    def login(self, username: str, password: str) -> None:
        """Log in with username and password"""
        self._run(self._async_client.login(username=username, password=password))

    def logout(self) -> None:
        """Logout of account"""
        self._run(self._async_client.logout())
