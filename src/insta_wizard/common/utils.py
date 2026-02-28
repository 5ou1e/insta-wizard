from __future__ import annotations

import base64
import re
from collections.abc import Iterator
from datetime import UTC, datetime
from functools import lru_cache
from typing import Any

import orjson
from babel import Locale

MASKED_EMAIL_RE = re.compile(
    r"(?i)(?<![A-Z0-9._%+\-])"
    r"(?=[^\s@]*\*[^\s@]*@|[^\s@]*@[^\s@]*\*[^\s@]*)"
    r"[A-Z0-9](?:[A-Z0-9._%+\-]|\*)*"
    r"@"
    r"(?:[A-Z0-9-]|\*)+(?:\.(?:[A-Z0-9-]|\*)+)+"
    r"(?![A-Z0-9._%+\-])"
)


def current_datetime() -> datetime:
    return datetime.now(UTC)


def dumps(data: dict | list) -> str:
    return orjson.dumps(data, option=orjson.OPT_NON_STR_KEYS).decode("utf-8")


def auth_data_from_authorization_header(authorization: str) -> dict:
    """Extract auth data dictionary from authorization header"""

    b64part = authorization.rsplit(":", 1)[-1]
    if not b64part:
        return {}
    return orjson.loads(base64.b64decode(b64part))


def normalize_locale_code(locale_code: str) -> str:
    s = locale_code.replace("-", "_")
    parts = s.split("_")
    if len(parts) == 2:
        return f"{parts[0].lower()}_{parts[1].upper()}"
    return s


@lru_cache(maxsize=512)
def display_name_for_locale(locale_code: str) -> str:
    loc = Locale.parse(normalize_locale_code(locale_code), sep="_", resolve_likely_subtags=False)
    lang_name = loc.get_display_name()
    lang_name = lang_name[:1].upper() + lang_name[1:] if lang_name else lang_name
    return lang_name


@lru_cache(maxsize=4096)
def locale_code_to_bcp47(locale_code: str) -> str:
    """
    ru_RU -> ru-RU
    en-us -> en-US
    en    -> en
    """
    s = locale_code.replace("_", "-")
    parts = s.split("-")
    if len(parts) == 1:
        return parts[0].lower()
    lang = parts[0].lower()
    region = parts[1].upper()
    return f"{lang}-{region}"


def iter_strings(obj: Any) -> Iterator[str]:
    """Рекурсивно отдаёт все строковые значения из dict/list/tuple."""
    if isinstance(obj, str):
        yield obj
        return

    if isinstance(obj, dict):
        for v in obj.values():
            yield from iter_strings(v)
        return

    if isinstance(obj, (list, tuple)):
        for v in obj:
            yield from iter_strings(v)
        return
