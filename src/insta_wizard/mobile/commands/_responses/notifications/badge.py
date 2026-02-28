from typing import TypedDict, Any


class _BadgeCountMap(TypedDict):
    di: int
    relationships: int
    activity_feed_dot_badge: int


class _BadgePayloadValue(TypedDict):
    total_count: int
    badge_count_map: _BadgeCountMap


class NotificationsBadgeResponse(TypedDict):
    badge_payload: dict[str, _BadgePayloadValue]
    status: str
