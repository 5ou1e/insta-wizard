from typing import Any, TypedDict


class AccountSecurityInfoResponse(TypedDict):
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
