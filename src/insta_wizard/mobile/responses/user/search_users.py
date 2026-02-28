from typing import Any, TypedDict


class _FriendshipStatus(TypedDict):
    following: bool
    is_bestie: bool
    is_feed_favorite: bool
    is_private: bool
    is_restricted: bool
    incoming_request: bool
    outgoing_request: bool


class _User(TypedDict):
    strong_id__: str
    pk: int
    pk_id: str
    fbid_v2: int
    third_party_downloads_enabled: int
    is_verified_search_boosted: bool
    id: str
    profile_pic_id: str
    profile_pic_url: str
    username: str
    full_name: str
    is_private: bool
    is_ring_creator: bool
    show_ring_award: bool
    has_anonymous_profile_picture: bool
    latest_reel_media: int
    account_badges: list[Any]
    is_verified: bool
    should_show_category: bool
    has_opt_eligible_shop: bool
    show_text_post_app_badge: bool
    unseen_count: int
    friendship_status: _FriendshipStatus


class UserSearchResponse(TypedDict):
    num_results: int
    users: list[_User]
    has_more: bool
    rank_token: str
    clear_client_cache: bool
    status: str
