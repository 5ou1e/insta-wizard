from typing import TypedDict, Any


class AttestationCreateAndroidKeystoreResponse(TypedDict):
    challenge_nonce: str
    key_nonce: str
    status: str
