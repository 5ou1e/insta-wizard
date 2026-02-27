from insta_wizard.common.exceptions import InstaWizardError
from insta_wizard.common.generators import generate_jazoest
from insta_wizard.common.logger import InstagramClientLogger, StdLoggingInstagramClientLogger
from insta_wizard.common.transport.aiohttp_transport import AioHttpTransport
from insta_wizard.common.transport.base import (
    HttpTransport,
)
from insta_wizard.common.transport.models import (
    TransportSettings,
)
from insta_wizard.common.models.proxy import ProxyInfo
from insta_wizard.web.commands.account.logout_ajax import AccountsLogoutAjax
from insta_wizard.web.common.command import (
    Command,
    CommandBus,
    R,
)
from insta_wizard.web.common.command_factories import (
    COMMAND_FACTORIES,
)
from insta_wizard.web.common.headers_factory import (
    WebClientHeadersFactory,
)
from insta_wizard.web.common.requesters.api_requester import (
    WebApiRequester,
)
from insta_wizard.web.common.requesters.web_navigator import (
    WebNavigator,
)
from insta_wizard.web.common.state_initializer import StateInitializer
from insta_wizard.web.flows import Login
from insta_wizard.web.models.deps import ClientDeps
from insta_wizard.web.models.device_info import (
    BrowserDeviceInfo,
    BrowserPreset,
)
from insta_wizard.web.models.local_data import WebClientLocalData
from insta_wizard.web.models.state import WebClientState
from insta_wizard.web.sections import (
    AccountSection,
    ChallengeSection,
    CommentsSection,
    FriendshipsSection,
    LikesSection,
    NavigationSection,
)


class WebInstagramClient:
    """Client for working with Instagram web API"""

    account: AccountSection
    challenge: ChallengeSection
    comments: CommentsSection
    friendships: FriendshipsSection
    likes: LikesSection
    navigation: NavigationSection

    def __init__(
        self,
        device: BrowserDeviceInfo | None = None,
        local_data: WebClientLocalData | None = None,
        proxy: ProxyInfo | None = None,
        transport_settings: TransportSettings | None = None,
        logger: InstagramClientLogger | None = None,
    ):
        device = device or BrowserDeviceInfo.from_preset(BrowserPreset.CHROME_143_WIN11)
        transport_settings = transport_settings or TransportSettings()

        self._logger = logger or StdLoggingInstagramClientLogger()
        local_data = local_data or WebClientLocalData()

        self.state = WebClientState(
            local_data=local_data,
            device=device,
        )

        self._transport = self._build_transport(
            settings=transport_settings,
            proxy=proxy,
        )
        self._headers = WebClientHeadersFactory(
            client_state=self.state,
        )
        self._api_requester = WebApiRequester(
            state=self.state,
            headers_factory=self._headers,
            transport=self._transport,
            logger=self._logger,
        )
        self._navigator = WebNavigator(
            state=self.state,
            headers_factory=self._headers,
            transport=self._transport,
            logger=self._logger,
        )

        self._bus = self._build_bus()

        self._initializer = StateInitializer(
            state=self.state,
            bus=self._bus,
        )

        deps = ClientDeps(
            state=self.state,
            transport=self._transport,
            logger=self._logger,
            initializer=self._initializer,
            navigator=self._navigator,
            api_requester=self._api_requester,
            headers=self._headers,
            bus=self._bus,
        )
        self._bus.bind_deps(deps)

        self.account = AccountSection(bus=self._bus, logger=self._logger)
        self.challenge = ChallengeSection(bus=self._bus, logger=self._logger)
        self.comments = CommentsSection(bus=self._bus, logger=self._logger)
        self.friendships = FriendshipsSection(bus=self._bus, logger=self._logger)
        self.likes = LikesSection(bus=self._bus, logger=self._logger)
        self.navigation = NavigationSection(bus=self._bus, logger=self._logger)

        self.state.local_data.set_cookies(
            {
                "ig_cb": "1",
                "ig_nrcb": "1",
                "wd": str(self.state.device.viewport_width)
                + "x"
                + str(self.state.device.viewport_height),
                "dpr": self.state.device.dpr,
            }
        )

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
            cookie_jar=self.state.local_data.cookie_jar,
        )

    async def __aenter__(self) -> "WebInstagramClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self._transport.close()

    def _build_bus(self) -> CommandBus:
        return CommandBus(factories=COMMAND_FACTORIES)

    async def execute(self, command: Command[R]) -> R:
        return await self._bus.execute(command)

    async def set_proxy(self, proxy: ProxyInfo | None) -> None:
        await self._transport.set_proxy(proxy_url=proxy.url if proxy else None)

    def get_cookies(self) -> dict:
        return self.state.local_data.cookies_as_dict()

    def set_cookies(self, cookies: dict) -> None:
        self.state.local_data.set_cookies(cookies)

    def get_local_data(self) -> WebClientLocalData:
        return self.state.local_data

    def dump_state(self) -> dict:
        """
        Serializes the current client state into a dict.
        Contains: browser parameters, session data and cookies.
        Does not contain: proxy and transport settings.

        Example::

            state = client.dump_state()
            with open("session.json", "wb") as f:
                f.write(orjson.dumps(state))

        """
        return {
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
            new_device = BrowserDeviceInfo.from_dict(state["device"])
            self.state.device = new_device
            self.state.local_data.load_from_dict(state["local_data"])
        except Exception as e:
            raise InstaWizardError(f"Failed to load client state: {e}") from e

    async def initialize_state(self):
        """Navigates to the home page and parses the parameters required for the client to work"""
        await self._initializer()

    async def login(self, username: str, password: str) -> None:
        """Log in to account using username and password"""
        return await self._bus.execute(Login(username=username, password=password))

    async def logout(self) -> None:
        """Logout of account"""
        if not self.state.sessionid:
            return
        await self._bus.execute(AccountsLogoutAjax(jazoest=generate_jazoest(self.state.csrftoken)))
