from typing import TypedDict, Any


class FriendshipsShowResponse(TypedDict):
    blocking: bool
    followed_by: bool
    following: bool
    incoming_request: bool
    is_bestie: bool
    is_blocking_reel: bool
    is_muting_reel: bool
    is_private: bool
    is_restricted: bool
    muting: bool
    outgoing_request: bool
    is_feed_favorite: bool
    subscribed: bool
    is_eligible_to_subscribe: bool
    is_supervised_by_viewer: bool
    is_guardian_of_viewer: bool
    is_muting_notes: bool
    is_muting_media_notes: bool
    is_muting_media_reposts: bool
    is_viewer_unconnected: bool
    status: str
