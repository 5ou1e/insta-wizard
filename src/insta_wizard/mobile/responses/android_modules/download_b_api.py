from typing import TypedDict


class ModulesItem(TypedDict):
    download_uri: str
    module_hash: str
    name: str


class AndroidModulesDownloadResponse(TypedDict):
    modules: list[ModulesItem]
    status: str
