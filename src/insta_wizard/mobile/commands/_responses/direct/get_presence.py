from typing import TypedDict, Any
class UserPresenceValue(TypedDict):
    capabilities: int
    copresence_enabled: None
    correlation_id: None
    is_active: bool
    last_activity_at_ms: int

class DirectV2GetPresenceResponse(TypedDict):
    status: str
    user_presence: dict[str, UserPresenceValue]
    status_code: str