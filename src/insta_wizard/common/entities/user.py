from typing import Any

from insta_wizard.common.entities.base import Entity


class User(Entity):
    """
    Core user identity, present in every API response that includes a user.
    """

    pk: int
    pk_id: str
    id: str
    strong_id__: str
    username: str
    full_name: str
    is_private: bool
    is_verified: bool
    profile_pic_url: str

    fbid_v2: int | None = None
    profile_pic_id: str | None = None
    has_anonymous_profile_picture: bool | None = None
    account_badges: list[Any] = []
    latest_reel_media: int | None = None
