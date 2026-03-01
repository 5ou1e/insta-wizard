from typing import Any

from insta_wizard.common.entities.base import Entity


class User(Entity):
    """
    Core user identity, present in every API response that includes a user.
    """

    pk: int
    id: str
    strong_id__: str
    username: str
    profile_pic_url: str

    pk_id: str | None = None
    full_name: str | None = None
    is_private: bool | None = None
    is_verified: bool | None = None

    fbid_v2: int | None = None
    profile_pic_id: str | None = None
    has_anonymous_profile_picture: bool | None = None
    account_badges: list[Any] = []
    latest_reel_media: int | None = None
