from __future__ import annotations

import secrets
import string
from functools import lru_cache

from insta_wizard.common.utils import locale_code_to_bcp47


def generate_web_session_id(part_len: int = 6) -> str:
    alphabet = string.ascii_lowercase + string.digits  # a-z0-9

    def part() -> str:
        return "".join(secrets.choice(alphabet) for _ in range(part_len))

    return f"{part()}:{part()}:{part()}"


@lru_cache(maxsize=4096)
def accept_language_from_locale(
    locale_code: str,
    fallbacks: tuple[str, ...] = ("en-US", "en"),
    q_start: float = 0.9,
    q_step: float = 0.1,
) -> str:
    """
    ru_RU -> "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    en_GB -> "en-GB,en;q=0.9"
    """
    primary = locale_code_to_bcp47(locale_code)
    base_lang = primary.split("-", 1)[0]

    tags: list[str] = []

    def add(tag: str) -> None:
        tag = locale_code_to_bcp47(tag)
        if tag and tag not in tags:
            tags.append(tag)

    add(primary)
    if "-" in primary:
        add(base_lang)

    if base_lang != "en":
        for fb in fallbacks:
            add(fb)

    out = [tags[0]]
    q = q_start
    for tag in tags[1:]:
        out.append(f"{tag};q={q:.1f}")
        q = max(0.1, q - q_step)

    return ",".join(out)
