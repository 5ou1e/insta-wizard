from typing import TypedDict


class UserGetLimitedInteractionsReminderResponse(TypedDict):
    show_limited_interactions_reminder: bool
    duration: int
    status: str
