from typing import Any, TypedDict


class FriendshipsUserFollowersResponseFriendRequests(TypedDict):
    pass


class FriendshipsUserFollowersResponseUsersItem(TypedDict):
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


class FriendshipsUserFollowersResponseGroupsItemFacepileItem(TypedDict):
    strong_id__: str
    pk: int
    pk_id: str
    full_name: str
    id: str
    username: str


class FriendshipsUserFollowersResponseGroupsItem(TypedDict):
    group: str
    title: str
    context: str
    facepile: list[FriendshipsUserFollowersResponseGroupsItemFacepileItem]
    subtitle: str
    subtitle_button_text: str
    category: str
    actions: list[str]
    show_hashtag_icon: bool


class FriendshipsUserFollowersResponse(TypedDict):
    users: list[FriendshipsUserFollowersResponseUsersItem]
    big_list: bool
    page_size: int
    groups: list[FriendshipsUserFollowersResponseGroupsItem]
    more_groups_available: bool
    friend_requests: FriendshipsUserFollowersResponseFriendRequests
    has_more: bool
    should_limit_list_of_followers: bool
    use_clickable_see_more: bool
    show_spam_follow_request_tab: bool
    follow_ranking_token: str
    status: str
