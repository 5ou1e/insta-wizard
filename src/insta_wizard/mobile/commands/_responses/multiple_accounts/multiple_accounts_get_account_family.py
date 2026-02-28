from typing import TypedDict, Any
class _CurrentAccount(TypedDict):
    strong_id__: str
    pk: int
    pk_id: str
    full_name: str
    has_password: int
    id: str
    username: str
    is_private: bool
    is_verified: bool
    profile_pic_id: str
    profile_pic_url: str
    has_onboarded_to_text_post_app: bool
    has_onboarded_to_basel: bool

class MultipleAcountsGetAccountFamilyResponse(TypedDict):
    child_accounts: list[Any]
    main_accounts: list[Any]
    current_account: _CurrentAccount
    status: str
