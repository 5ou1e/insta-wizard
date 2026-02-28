from __future__ import annotations

from insta_wizard.common.entities.base import Entity
from insta_wizard.common.entities.user import User


class SentDirectMessage(Entity):
    """Acknowledgment returned by the send message endpoint."""

    item_id: str
    thread_id: str
    timestamp: str
    client_context: str
    msg_id: str


class DirectMessage(Entity):
    """A single message item inside a direct thread."""

    item_id: str
    user_id: str
    timestamp: int
    item_type: str
    is_sent_by_viewer: bool
    is_shh_mode: bool | None = None
    is_disappearing: bool | None = None
    client_context: str | None = None
    text: str | None = None


class DirectThread(Entity):
    """A direct messaging thread (DM or group chat)."""

    thread_id: str
    thread_v2_id: str
    thread_type: str
    thread_title: str
    is_group: bool
    users: list[User]
    folder: int
    read_state: int
    muted: bool
    archived: bool
    pending: bool
    last_activity_at: int
    last_permanent_item: DirectMessage | None = None
    items: list[DirectMessage]
