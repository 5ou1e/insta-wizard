from typing import TypedDict


class AccountGetPresenceDisabledResponse(TypedDict):
    disabled: bool
    thread_presence_disabled: bool
    copresence_disabled: bool
    public_presence_enabled_for_business_user: bool
    status: str
