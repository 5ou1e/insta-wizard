from __future__ import annotations

from insta_wizard.common.exceptions import InstaWizardError
from insta_wizard.common.logger import InstagramClientLogger, StdLoggingInstagramClientLogger
from insta_wizard.common.models import ProxyInfo
from insta_wizard.common.transport.aiohttp_transport import AioHttpTransport
from insta_wizard.common.transport.base import (
    HttpTransport,
)
from insta_wizard.common.transport.models import (
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
from insta_wizard.mobile.flows import BloksLogin
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

        self._bus = CommandBus(factories=COMMAND_FACTORIES)

        graph_deps = {
            "state": self.state,
            "request_executor": self._request_executor,
            "headers": self._headers,
        }
        self._graphql_www = GraphqlWWW(**graph_deps)
        self._graphql_query = GraphqlQuery(**graph_deps)

        self.account = AccountSection(bus=self._bus)
        self.users = UserSection(bus=self._bus)
        self.friendships = FriendshipsSection(bus=self._bus)
        self.feed = FeedSection(bus=self._bus)
        self.direct = DirectSection(bus=self._bus)
        self.media = MediaSection(bus=self._bus)
        self.notifications = NotificationSection(bus=self._bus)
        self.news = NewsSection(bus=self._bus)
        self.live = LiveSection(bus=self._bus)
        self.clips = ClipSection(bus=self._bus)
        self.challenge = ChallengeSection(bus=self._bus)

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

    async def execute(self, command: Command[R]) -> R:
        return await self._bus.execute(command)

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
        Сериализует текущее состояние клиента в dict.
        Содержит: версию приложения, параметры устройства, сессионные данные.
        Не содержит: прокси, настройки транспорта, логгер — они передаются при создании клиента.

        Пример сохранения::

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
        Восстанавливает состояние клиента из dict, полученного через dump_state().
        Транспорт, прокси и логгер остаются неизменными.

        Пример загрузки::

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
            raise InstaWizardError(f"Не удалось загрузить MobileClientState: {e}") from e

    async def login(self, username: str, password: str):
        return await self._bus.execute(BloksLogin(username=username, password=password))
