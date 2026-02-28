from typing import TypedDict, Any


class ModulesItem(TypedDict):
    download_uri: str
    module_hash: str
    name: str


class AndroidModulesDownloadResponse(TypedDict):
    modules: list[ModulesItem]
    status: str
