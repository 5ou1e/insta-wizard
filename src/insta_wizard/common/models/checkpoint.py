from dataclasses import dataclass
from enum import StrEnum
from typing import TypeAlias, Union, ClassVar


class CheckpointType(StrEnum):
    UNKNOWN = "UNKNOWN"  # Неизвестный для нас чекпоинт
    UFAC_WWW_BLOKS = "UFAC_WWW_BLOKS"
    VETTED_DELTA = "VETTED_DELTA"  # delta_login_review
    SCRAPING_WARNING = "SCRAPING_WARNING"


class UnknownCheckpointStep(StrEnum):
    UNKNOWN = "UNKNOWN"


class UfacStep(StrEnum):
    UNKNOWN = "UNKNOWN"
    INTRO = "INTRO"
    CAPTCHA = "CAPTCHA"
    SET_CONTACT_POINT = "SET_CONTACT_POINT"
    CODE_SUBMIT = "CODE_SUBMIT"
    SELFIE = "SELFIE"
    DONE = "DONE"
    DISABLED = "DISABLED"


class VettedDeltaStep(StrEnum):
    UNKNOWN = "UNKNOWN"


class ScrapingWarningStep(StrEnum):
    UNKNOWN = "UNKNOWN"


@dataclass(slots=True)
class UfacCheckpoint:
    type: ClassVar[CheckpointType] = CheckpointType.UFAC_WWW_BLOKS
    step: UfacStep = UfacStep.UNKNOWN


@dataclass(slots=True)
class VettedDeltaCheckpoint:
    type: ClassVar[CheckpointType] = CheckpointType.VETTED_DELTA
    step: VettedDeltaStep = VettedDeltaStep.UNKNOWN


@dataclass(slots=True)
class ScrapingWarningCheckpoint:
    type: ClassVar[CheckpointType] = CheckpointType.SCRAPING_WARNING
    step: ScrapingWarningStep = ScrapingWarningStep.UNKNOWN


@dataclass(kw_only=True, slots=True)
class UnknownCheckpoint:
    type: ClassVar[CheckpointType] = CheckpointType.UNKNOWN
    step: UnknownCheckpointStep = UnknownCheckpointStep.UNKNOWN
    response: dict | None = None


Checkpoint: TypeAlias = Union[
    UnknownCheckpoint,
    UfacCheckpoint,
    VettedDeltaCheckpoint,
    ScrapingWarningCheckpoint,
]
