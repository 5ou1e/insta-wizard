import json
import re

import orjson

from insta_wizard.common.models.other import EncryptionInfo
from insta_wizard.web.commands.navigation.get_home_page import (
    GetInstagramHomePage,
)
from insta_wizard.web.common.command import CommandBus
from insta_wizard.web.exceptions import ResponseParsingError
from insta_wizard.web.models.other import GraphqlQueriesInitialParams
from insta_wizard.web.models.state import WebClientState


class StateInitializer:
    def __init__(self, state: WebClientState, bus: CommandBus):
        self.state = state
        self.bus = bus

    async def __call__(self):
        """Navigates to the home page and parses the parameters required for the client to work"""

        response = await self.bus.execute(GetInstagramHomePage())

        m = re.search(r'"rollout_hash"\s*:\s*"([^"]+)"', response)
        ajax_hash = m.group(1) if m else None
        if not ajax_hash:
            raise ResponseParsingError(msg="Не удалось спарсить rollout_hash из ответа инстаграм")

        m = re.search(r'"machine_id"\s*:\s*"([^"]+)"', response)
        machine_id = m.group(1) if m else None
        if not machine_id:
            raise ResponseParsingError(msg="Не удалось спарсить machine_id из ответа инстаграм")

        self.state.local_data.ajax_hash = ajax_hash
        self.state.local_data.set_cookies({"mid": machine_id})
        self.state.encryption_info = extract_instagram_password_encryption(response)
        self.state.initial_params = extract_initial_params_from_html(response)


def extract_instagram_password_encryption(html: str) -> EncryptionInfo:
    needle = '"InstagramPasswordEncryption"'
    pos = html.find(needle)

    err_message = "Не удалось извлечь InstagramPasswordEncryption параметры из ответа инстаграм"
    if pos == -1:
        raise ResponseParsingError(msg=err_message)

    brace = html.find("{", pos)
    if brace == -1:
        raise ResponseParsingError(msg=err_message)

    obj, _ = json.JSONDecoder().raw_decode(html[brace:])

    return EncryptionInfo(
        publickeyid=int(obj["key_id"]),
        publickey=obj["public_key"],
        version=int(obj["version"]),
    )


def extract_initial_params_from_html(html: str):
    def find1(pattern: str, *, flags=re.S) -> str:
        m = re.search(pattern, html, flags)
        if not m:
            raise ResponseParsingError(
                msg="Не удалось извлечь graphql initial-params из ответа инстаграм"
            )
        return m.group(1)

    lsd_token = find1(r'\["LSD",\s*\[\s*\],\s*\{"token":"([^"]+)"\}')

    dtsg_token = extract_dtsg(html)

    site_data_json = find1(r'\["SiteData",\s*\[\s*\],\s*(\{.*?\})\s*,\s*\d+\s*\]')
    site_data = orjson.loads(site_data_json)

    haste_session = str(site_data["haste_session"])
    hsi = str(site_data["hsi"])
    spin_r = str(site_data["__spin_r"])
    spin_b = str(site_data["__spin_b"])
    spin_t = str(site_data["__spin_t"])
    comet_env = str(site_data["comet_env"])

    versioning_id = find1(r'\["WebBloksVersioningID",\s*\[\s*\],\s*\{"versioningID":"([^"]+)"\}')

    jazoest = find1(r"[?&]jazoest=(\d+)")

    return GraphqlQueriesInitialParams(
        lsd_token=lsd_token,
        dtsg_token=dtsg_token,
        haste_session=haste_session,
        hsi=hsi,
        spin_r=spin_r,
        spin_b=spin_b,
        spin_t=spin_t,
        comet_env=comet_env,
        versioning_id=versioning_id,
        jazoest=jazoest,
    )


def extract_dtsg(html: str) -> str | None:
    m = re.search(
        r'\["DTSGInitData",\s*\[\s*\],\s*\{"token":"([^"]*)","async_get_token":"([^"]*)"\}',
        html,
        re.S,
    )
    if m:
        token = m.group(1)
        return token

    m = re.search(
        r'\["DTSGInitialData",\s*\[\s*\],\s*\{"token":"([^"]*)"\}',
        html,
        re.S,
    )
    if m:
        token = m.group(1)
        return token

    m = re.search(r'name="fb_dtsg"\s+value="([^"]+)"', html)
    if m:
        return m.group(1)

    return None
