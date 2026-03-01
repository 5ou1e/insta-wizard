from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from insta_wizard.common.logger import InstagramClientLogger
from insta_wizard.common.transport.base import HttpTransport
from insta_wizard.mobile.common.mobile_requester import (
    MobileRequester,
)
from insta_wizard.mobile.models.state import MobileClientState
from insta_wizard.mobile.sections.graphql_query import (
    GraphqlQuery,
)
from insta_wizard.mobile.sections.graphql_www import GraphqlWWW

if TYPE_CHECKING:
    from insta_wizard.mobile.common.command import CommandBus


@dataclass(slots=True)
class ClientDeps:
    state: MobileClientState
    logger: InstagramClientLogger
    http: HttpTransport
    requester: MobileRequester

    graphql_www: GraphqlWWW
    graphql_query: GraphqlQuery

    bus: CommandBus  # type: ignore[name-defined]
