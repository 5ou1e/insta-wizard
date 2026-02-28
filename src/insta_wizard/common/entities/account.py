from typing import Any

from insta_wizard.common.entities.base import Entity


class Account(Entity):
    """Authenticated user's own account.

    Returned by account/current_user endpoint. Contains personal fields
    (email, phone, birthday) that are not available on public User profiles.
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

    # Private contact info (only available for own account)
    email: str
    phone_number: str
    birthday: str
    gender: int
    pronouns: list[Any]

    # Public profile
    biography: str
    external_url: str
    bio_links: list[Any]
    is_business: bool

    is_quiet_mode_enabled: bool

    # Optional
    profile_pic_id: str | None = None
    fbid_v2: int | None = None
    has_anonymous_profile_picture: bool | None = None
    category: str | None = None
    custom_gender: str | None = None
    country_code: int | None = None
    national_number: int | None = None
    account_type: int | None = None
    allowed_commenter_type: str | None = None
    reel_auto_archive: str | None = None


class AccountSecurity(Entity):
    phone_number: str
    country_code: str
    national_number: str
    is_phone_confirmed: bool
    is_two_factor_enabled: bool
    is_totp_two_factor_enabled: bool
    is_trusted_notifications_enabled: bool
    is_eligible_for_whatsapp_two_factor: bool
    is_whatsapp_two_factor_enabled: bool
    backup_codes: None
    trusted_devices: list[Any]
    has_reachable_email: bool
    eligible_for_trusted_notifications: bool
    email: str
    is_eligible_for_multiple_totp: bool
    totp_seeds: list[Any]
    can_add_additional_totp_seed: bool
    is_eligible_for_phone_number_confirmed_badge_toggle: bool
    is_phone_number_confirmed_badge_enabled: bool
    status: str
