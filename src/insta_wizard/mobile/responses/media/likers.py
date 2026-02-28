from typing import Any, TypedDict


class _User(TypedDict):
    strong_id__: str
    pk: int
    pk_id: str
    id: str
    username: str
    full_name: str
    is_private: bool
    is_verified: bool
    profile_pic_url: str
    account_badges: list[Any]
    latest_reel_media: int


class MediaLikersResponse(TypedDict):
    users: list[_User]
    user_count: int
    play_count: int
    follow_ranking_token: str
    status: str
