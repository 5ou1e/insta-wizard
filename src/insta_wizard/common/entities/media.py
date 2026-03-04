from dataclasses import dataclass
from typing import Literal

from pydantic import AliasChoices, Field, field_validator

from insta_wizard.common.entities import Entity


class Media(Entity):
    pk: str
    id: str
    code: str
    media_type: int  # 1=photo  2=video  8=carousel
    taken_at: int
    width: int = Field(validation_alias=AliasChoices("width", "original_width"))
    height: int = Field(validation_alias=AliasChoices("height", "original_height"))
    # feed + carousel
    caption: str | None = None
    like_count: int | None = None
    comment_count: int | None = None
    # story
    expiring_at: int | None = None
    viewer_count: int | None = None
    # carousel
    item_count: int | None = None
    item_pks: list[int] | None = None

    @field_validator("caption", mode="before")
    @classmethod
    def extract_caption_text(cls, v: object) -> str | None:
        if isinstance(v, dict):
            return v.get("text")
        return v  # type: ignore[return-value]

    @property
    def url(self) -> str:
        return f"https://www.instagram.com/p/{self.code}/"


@dataclass(slots=True, kw_only=True)
class AlbumPhotoItem:
    """A photo item for a carousel album."""

    image_bytes: bytes


@dataclass(slots=True, kw_only=True)
class AlbumVideoItem:
    """A video item for a carousel album.

    Args:
        video_bytes: Raw video file bytes.
        thumbnail_bytes: Custom cover image. Auto-extracted if not provided.
        transcode: Re-encode to H.264/yuv420p if needed.
        fit_mode: How to handle out-of-bounds aspect ratios. "pad" or "crop".
    """

    video_bytes: bytes
    thumbnail_bytes: bytes | None = None
    transcode: bool = True
    fit_mode: Literal["pad", "crop"] = "pad"
