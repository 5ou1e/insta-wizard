from typing import TypedDict


class _ItemsItem(TypedDict):
    title: str
    ui_type: str
    content_type: str
    icon: str
    checked: bool
    setting_value: str
    channel: str


class _SectionsItem(TypedDict):
    title: str
    items: list[_ItemsItem]
    content_type: str


class NotificationsGetNotificationSettingsResponse(TypedDict):
    sections: list[_SectionsItem]
    status: str
