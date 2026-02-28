from insta_wizard.common.entities.base import Entity


class FriendshipStatusShort(Entity):
    """Lightweight friendship status returned by batch endpoints (e.g. show_many)."""

    following: bool
    incoming_request: bool
    outgoing_request: bool
    is_private: bool
    is_restricted: bool
    is_bestie: bool
    is_feed_favorite: bool


class FriendshipStatus(FriendshipStatusShort):
    """Full friendship status returned by follow/unfollow/show endpoints."""

    followed_by: bool
    muting: bool
    blocking: bool
    is_eligible_to_subscribe: bool
    subscribed: bool

    # Only available from the dedicated friendships_show endpoint
    is_muting_reel: bool | None = None
    is_blocking_reel: bool | None = None
    is_muting_notes: bool | None = None
    is_muting_media_notes: bool | None = None
    is_muting_media_reposts: bool | None = None
    is_supervised_by_viewer: bool | None = None
    is_guardian_of_viewer: bool | None = None
    is_viewer_unconnected: bool | None = None
