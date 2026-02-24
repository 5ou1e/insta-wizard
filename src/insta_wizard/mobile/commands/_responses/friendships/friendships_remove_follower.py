from typing import TypedDict


class FriendshipsRemoveFollowerResponseFriendshipStatus(TypedDict):
    following: bool
    is_bestie: bool
    is_feed_favorite: bool
    is_private: bool
    is_restricted: bool
    incoming_request: bool
    outgoing_request: bool
    followed_by: bool
    muting: bool
    blocking: bool
    is_eligible_to_subscribe: bool
    subscribed: bool


class FriendshipsRemoveFollowerResponse(TypedDict):
    friendship_status: FriendshipsRemoveFollowerResponseFriendshipStatus
    previous_following: None
    error: None
    status: str
