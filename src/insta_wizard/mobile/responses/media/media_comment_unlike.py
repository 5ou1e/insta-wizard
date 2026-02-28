from typing import TypedDict


class _Comment(TypedDict):
    has_liked_comment: bool


class MediaCommentUnlikeResponse(TypedDict):
    comment: _Comment
    status: str
