from typing import TypedDict


class AccountSendConfirmEmailResponse(TypedDict):
    is_email_legit: bool
    title: str
    body: str
    status: str
