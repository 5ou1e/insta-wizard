from typing import Any, TypedDict


class FriendshipsUserFollowingResponseUsersItem(TypedDict):
    strong_id__: str
    pk: int
    pk_id: str
    id: str
    full_name: str
    fbid_v2: int
    third_party_downloads_enabled: int
    profile_pic_id: str
    profile_pic_url: str
    is_verified: bool
    username: str
    is_private: bool
    has_anonymous_profile_picture: bool
    account_badges: list[Any]
    latest_reel_media: int
    is_favorite: bool


class FriendshipsUserFollowingResponse(TypedDict):
    users: list[FriendshipsUserFollowingResponseUsersItem]
    big_list: bool
    page_size: int
    next_max_id: str
    has_more: bool
    should_limit_list_of_followers: bool
    use_clickable_see_more: bool
    show_spam_follow_request_tab: bool
    follow_ranking_token: str
    status: str
