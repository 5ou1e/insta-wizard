from typing import TypedDict

from insta_wizard.mobile.commands._responses.media.media_comment_like import (
    MediaCommentLikeResponseComment,
)


class MediaCommentUnlikeResponseComment(TypedDict):
    has_liked_comment: bool


class MediaCommentUnlikeResponse(TypedDict):
    comment: MediaCommentLikeResponseComment
    status: str
