from __future__ import annotations

from insta_wizard.common.exceptions import InstaWizardError
from insta_wizard.common.logger import InstagramClientLogger, StdLoggingInstagramClientLogger
from insta_wizard.common.models.proxy import ProxyInfo
from insta_wizard.common.transport.aiohttp_transport import AioHttpTransport
from insta_wizard.common.transport.base import (
    HttpTransport,
)
from insta_wizard.common.transport.models import (
    HttpMethod,
    TransportSettings,
)
from insta_wizard.mobile.common.command import (
    Command,
    CommandBus,
    R,
)
from insta_wizard.mobile.common.command_factories import (
    COMMAND_FACTORIES,
)
from insta_wizard.mobile.common.headers_factory import (
    MobileClientHeadersFactory,
)
from insta_wizard.mobile.common.requesters.api_requester import (
    ApiRequestExecutor,
)
from insta_wizard.mobile.common.requesters.requester import (
    RequestExecutor,
)
from insta_wizard.mobile.models.android_device_info import (
    AndroidDeviceInfo,
    AndroidPreset,
)
from insta_wizard.mobile.models.deps import ClientDeps
from insta_wizard.mobile.models.local_data import (
    MobileClientLocalData,
)
from insta_wizard.mobile.models.state import MobileClientState
from insta_wizard.mobile.models.version import InstagramAppVersion, InstagramAppVersionInfoRegistry
from insta_wizard.mobile.sections import (
    AccountSection,
    ChallengeSection,
    ClipSection,
    DirectSection,
    FeedSection,
    FriendshipsSection,
    LiveSection,
    MediaSection,
    NewsSection,
    NotificationSection,
    UserSection,
)
from insta_wizard.mobile.sections.graphql_query import (
    GraphqlQuery,
)
from insta_wizard.mobile.sections.graphql_www import GraphqlWWW


class MobileInstagramClient:
    """Client for working with Instagram private API"""

    account: AccountSection
    users: UserSection
    friendships: FriendshipsSection
    feed: FeedSection
    direct: DirectSection
    media: MediaSection
    notifications: NotificationSection
    news: NewsSection
    live: LiveSection
    clips: ClipSection
    challenge: ChallengeSection

    def __init__(
        self,
        device: AndroidDeviceInfo | None = None,
        version: InstagramAppVersion = InstagramAppVersion.V374,
        local_data: MobileClientLocalData | None = None,
        proxy: ProxyInfo | None = None,
        transport_settings: TransportSettings | None = None,
        logger: InstagramClientLogger | None = None,
    ):
        if version not in self._supported_versions():
            raise ValueError(
                f"Version {version} not supported. "
                f"Available versions: {', '.join(self._supported_versions())}"
            )

        device = device or AndroidDeviceInfo.from_preset(AndroidPreset.SAMSUNG_A16)
        local_data = local_data or MobileClientLocalData.create()
        self._logger = logger or StdLoggingInstagramClientLogger()
        self.state = MobileClientState(
            device=device,
            local_data=local_data,
            version_info=InstagramAppVersionInfoRegistry.get(version),
        )
        self._headers = MobileClientHeadersFactory(state=self.state)

        transport_settings = transport_settings or TransportSettings()
        self._transport = self._build_transport(settings=transport_settings, proxy=proxy)

        self._request_executor = RequestExecutor(
            client_state=self.state,
            transport=self._transport,
            logger=self._logger,
        )
        self._api_request_executor = ApiRequestExecutor(
            client_state=self.state,
            transport=self._transport,
            logger=self._logger,
        )

        self._bus = self._build_bus()

        graph_deps = {
            "state": self.state,
            "request_executor": self._request_executor,
            "headers": self._headers,
        }
        self._graphql_www = GraphqlWWW(**graph_deps)
        self._graphql_query = GraphqlQuery(**graph_deps)

        self.account = AccountSection(state=self.state, bus=self._bus)
        self.users = UserSection(state=self.state, bus=self._bus)
        self.friendships = FriendshipsSection(state=self.state, bus=self._bus)
        self.feed = FeedSection(state=self.state, bus=self._bus)
        self.direct = DirectSection(state=self.state, bus=self._bus)
        self.media = MediaSection(state=self.state, bus=self._bus)
        self.notifications = NotificationSection(state=self.state, bus=self._bus)
        self.news = NewsSection(state=self.state, bus=self._bus)
        self.live = LiveSection(state=self.state, bus=self._bus)
        self.clips = ClipSection(state=self.state, bus=self._bus)
        self.challenge = ChallengeSection(
            state=self.state, bus=self._bus, graphql_www=self._graphql_www, logger=self._logger
        )

        deps = ClientDeps(
            http=self._transport,
            req=self._request_executor,
            api=self._api_request_executor,
            state=self.state,
            headers=self._headers,
            graphql_www=self._graphql_www,
            graphql_query=self._graphql_query,
            logger=self._logger,
            bus=self._bus,
        )

        self._bus.bind_deps(deps)

    def _supported_versions(self) -> frozenset[InstagramAppVersion]:
        return frozenset({InstagramAppVersion.V374})

    def _build_transport(
        self,
        settings: TransportSettings,
        proxy: ProxyInfo | None = None,
    ) -> HttpTransport:
        return AioHttpTransport(
            settings=settings,
            logger=self._logger,
            proxy_url=proxy.url if proxy else None,
            timeout=settings.max_network_wait_time,
        )

    def _build_bus(self) -> CommandBus:
        return CommandBus(factories=COMMAND_FACTORIES)

    async def execute(self, command: Command[R]) -> R:
        return await self._bus.execute(command)

    async def custom_request(
        self,
        method: HttpMethod,
        url: str,
        data: dict | bytes | None = None,
        params: dict | None = None,
        extra_headers: dict | None = None,
    ) -> dict:
        """Make a raw API request with default mobile headers applied."""
        return await self._api_request_executor.call_url(
            method=method,
            url=url,
            data=data,
            params=params,
            extra_headers=extra_headers,
        )

    async def __aenter__(self) -> MobileInstagramClient:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self._transport.close()

    async def set_proxy(self, proxy: ProxyInfo | None) -> None:
        await self._transport.set_proxy(proxy_url=proxy.url if proxy else None)

    def get_local_data(self) -> MobileClientLocalData:
        return self.state.local_data

    def dump_state(self) -> dict:
        """
        Serializes the current client state into a dict.
        Contains: app version, device parameters, session data.

        Example::

            state = client.dump_state()
            with open("session.json", "wb") as f:
                f.write(orjson.dumps(state))

        """
        return {
            "version": self.state.version_info.version.value,
            "device": self.state.device.to_dict(),
            "local_data": self.state.local_data.to_dict(),
        }

    def load_state(self, state: dict) -> None:
        """
        Restores client state from a dict obtained via dump_state().

        Example::

            with open("session.json", "rb") as f:
                state = orjson.loads(f.read())
            client.load_state(state)

        """
        try:
            new_version_info = InstagramAppVersionInfoRegistry.get(
                InstagramAppVersion(state["version"])
            )
            new_device = AndroidDeviceInfo.from_dict(state["device"])
            new_local_data = MobileClientLocalData.from_dict(state["local_data"])

            self.state.device = new_device
            self.state.local_data = new_local_data
            self.state.version_info = new_version_info
        except Exception as e:
            raise InstaWizardError(f"Failed to load client state: {e}") from e

    async def login(self, username: str, password: str):
        """Log in with username and password"""
        return await self.account.login(
            username=username,
            password=password,
        )

    async def logout(self) -> None:
        """Logout of account"""
        return await self.account.logout()
