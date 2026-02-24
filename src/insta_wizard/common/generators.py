from __future__ import annotations

import base64
import hashlib
import hmac
import random
import string
import time
import uuid
from datetime import UTC, datetime

import pytz


def current_timestamp() -> int:
    return int(datetime.now(UTC).timestamp())


def current_timestamp_str() -> str:
    return str(current_timestamp())


def current_timestamp_ms() -> int:
    return int(time.time() * 1000)


def timestamp_with_ms_str(decimals=3) -> str:
    """1753084231.273"""
    return f"{time.time():.{decimals}f}"


def uuid_v4_hex() -> str:
    return uuid.uuid4().hex


def generate_uuid_v4_string():
    return str(uuid.uuid4())


def generate_jazoest(symbols: str) -> str:
    amount = sum(ord(s) for s in symbols)
    return f"2{amount}"


def utc_offset_from_timezone(timezone: str) -> int:
    """Возвращает разницу часовых поясов в секундах"""

    now = datetime.now(pytz.timezone(timezone))
    return int(now.utcoffset().total_seconds())


def gen_user_breadcrumb(size: int) -> str:
    """
    Generates user breadcrumbs
    """

    key = "iN4$aGr0m"
    dt = int(time.time() * 1000)
    time_elapsed = random.randint(500, 1500) + size * random.randint(500, 1500)
    text_change_event_count = max(1, size / random.randint(3, 5))
    data = "{size!s} {elapsed!s} {count!s} {dt!s}".format(
        **{
            "size": size,
            "elapsed": time_elapsed,
            "count": text_change_event_count,
            "dt": dt,
        }
    )
    return "{!s}\n{!s}\n".format(
        base64.b64encode(
            hmac.new(key.encode("ascii"), data.encode("ascii"), digestmod=hashlib.sha256).digest()
        ),
        base64.b64encode(data.encode("ascii")),
    )


def generate_token(size=10, symbols=False):
    chars = string.ascii_letters + string.digits
    if symbols:
        chars += string.punctuation
    return "".join(random.choice(chars) for _ in range(size))


def generate_waterfall_id():
    return str(uuid.uuid4())


def generate_android_id_from_guid(guid: uuid.UUID | str) -> str:
    """
    Generates AndroidID for UUID
    """

    md5_hash = hashlib.md5(str(guid).encode()).hexdigest()
    return f"android-{md5_hash[:16]}"
