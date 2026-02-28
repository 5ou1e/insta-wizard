from typing import TypedDict


class AttestationCreateAndroidKeystoreResponse(TypedDict):
    challenge_nonce: str
    key_nonce: str
    status: str
