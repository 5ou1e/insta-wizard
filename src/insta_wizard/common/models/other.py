from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class EncryptionInfo:
    """Password encryption info"""

    publickeyid: int
    publickey: str
    version: int
