from collections.abc import Iterable
from dataclasses import dataclass, field

from aiohttp import CookieJar
from yarl import URL

from insta_wizard.web.common.constants import WWW_INSTAGRAM_URL
from insta_wizard.web.common.utils import generate_web_session_id


@dataclass(kw_only=True, slots=True)
class WebClientLocalData:
    www_claim: str | None = None
    ajax_hash: str | None = None
    web_session_id: str = field(
        default_factory=generate_web_session_id
    )  # неизвестно откуда это берется - просто генерим

    cookie_jar: CookieJar = field(default_factory=CookieJar)

    @classmethod
    def create(
        cls,
        www_claim: str | None = None,
        ajax_hash: str | None = None,
        web_session_id: str | None = None,
        cookies: dict | None = None,
    ) -> "WebClientLocalData":
        if not web_session_id:
            web_session_id = generate_web_session_id()

        cookie_jar = CookieJar()

        data = cls(
            www_claim=www_claim,
            ajax_hash=ajax_hash,
            web_session_id=web_session_id or generate_web_session_id(),
            cookie_jar=cookie_jar,
        )

        if cookies:
            data.set_cookies(dict(cookies))

        return data

    def get_cookie(self, name: str, default: str | None = None) -> str | None:
        jar = self.cookie_jar.filter_cookies(URL(WWW_INSTAGRAM_URL))

        morsel = jar.get(name)
        if morsel:
            return morsel.value

        target = name.lower()
        for k, v in jar.items():
            if k.lower() == target:
                return v.value

        return default

    def set_cookies(self, cookies: dict[str, str] | None) -> None:
        if not cookies:
            return
        self.cookie_jar.update_cookies(cookies, response_url=URL(WWW_INSTAGRAM_URL))

    def clear_cookies(self, names: Iterable[str]) -> None:
        names_l = {n.lower() for n in names}
        self.cookie_jar.clear(lambda m: (m.key or "").lower() in names_l)

    def cookies_as_dict(self) -> dict[str, str]:
        jar = self.cookie_jar.filter_cookies(URL(WWW_INSTAGRAM_URL))
        return {k: v.value for k, v in jar.items()}

    def cookies_as_string(self) -> str:
        d = self.cookies_as_dict()
        return ";".join(f"{k}={v}" for k, v in d.items())

    def to_dict(self) -> dict:
        return {
            "www_claim": self.www_claim,
            "ajax_hash": self.ajax_hash,
            "web_session_id": self.web_session_id,
            "cookies": self.cookies_as_dict(),
        }

    def load_from_dict(self, data: dict) -> None:
        """Update this instance in-place from dict (preserves cookie_jar reference)."""
        self.www_claim = data.get("www_claim")
        self.ajax_hash = data.get("ajax_hash")
        self.web_session_id = data.get("web_session_id") or generate_web_session_id()
        cookies = data.get("cookies")
        if cookies:
            self.cookie_jar.clear()
            self.set_cookies(cookies)
