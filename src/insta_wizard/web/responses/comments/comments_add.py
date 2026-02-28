from typing import TypedDict


class _From(TypedDict):
    id: str
    username: str
    full_name: str
    profile_picture: str


class CommentsAddResponse(TypedDict):
    id: str
    from_: _From
    text: str
    created_time: int
    status: str
