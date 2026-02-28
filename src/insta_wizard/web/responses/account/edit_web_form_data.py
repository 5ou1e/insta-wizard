from typing import Any, TypedDict


class _Username(TypedDict):
    should_show_confirmation_dialog: bool
    is_pending_review: bool
    confirmation_dialog_text: str
    disclaimer_text: str


class _ProfileEditParams(TypedDict):
    username: _Username
    full_name: _Username


class _FormData(TypedDict):
    first_name: str
    last_name: str
    email: str
    is_email_confirmed: bool
    is_phone_confirmed: bool
    username: str
    phone_number: str
    gender: int
    birthday: str
    fb_birthday: str
    biography: str
    bio_links_for_web_edit_only: list[Any]
    external_url: str
    chaining_enabled: bool
    presence_disabled: bool
    business_account: bool
    usertag_review_enabled: bool
    custom_gender: str
    trusted_username: str
    trust_days: int
    profile_edit_params: _ProfileEditParams


class AccountsEditWebFormDataResponse(TypedDict):
    form_data: _FormData
    status: str
