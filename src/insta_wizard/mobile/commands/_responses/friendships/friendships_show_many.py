from collections.abc import Mapping
from typing import TypedDict


class FriendshipsShowManyResponseFriendshipStatus(TypedDict):
    following: bool
    incoming_request: bool
    is_bestie: bool
    is_private: bool
    is_restricted: bool
    outgoing_request: bool
    is_feed_favorite: bool


class FriendshipsShowManyResponse(TypedDict):
    friendship_statuses: Mapping[str, FriendshipsShowManyResponseFriendshipStatus]
    status: str
