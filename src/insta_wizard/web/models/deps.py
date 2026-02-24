from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from insta_wizard.common.logger import InstagramClientLogger
from insta_wizard.common.transport.base import HttpTransport
from insta_wizard.web.common.headers_factory import (
    WebClientHeadersFactory,
)
from insta_wizard.web.common.requesters.api_requester import (
    WebApiRequester,
)
from insta_wizard.web.common.requesters.web_navigator import (
    WebNavigator,
)
from insta_wizard.web.common.state_initializer import (
    StateInitializer,
)
from insta_wizard.web.models.state import WebClientState

if TYPE_CHECKING:
    from insta_wizard.web.common.command import CommandBus


@dataclass(slots=True)
class ClientDeps:
    state: WebClientState
    transport: HttpTransport
    logger: InstagramClientLogger
    initializer: StateInitializer
    navigator: WebNavigator
    api_requester: WebApiRequester
    headers: WebClientHeadersFactory

    bus: CommandBus  # type: ignore[name-defined]
