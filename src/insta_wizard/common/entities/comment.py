from insta_wizard.common.entities.base import Entity
from insta_wizard.common.entities.user import User


class Comment(Entity):
    """A comment on a media post."""

    pk: str
    strong_id__: str
    text: str
    user_id: str
    user: User
    type: int
    created_at: int
    created_at_utc: int
    content_type: str
    status: str
    bit_flags: int
    share_enabled: bool
    is_text_editable: bool
    did_report_as_spam: bool

    # Only present when fetching comments list, absent on newly created comment
    media_id: int | None = None
    comment_like_count: int | None = None
    child_comment_count: int | None = None
    has_liked_comment: bool | None = None
    is_ranked_comment: bool | None = None
    is_edited: bool | None = None
    private_reply_status: int | None = None
