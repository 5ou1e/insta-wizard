"""
Logging configuration — works with both MobileInstagramClient and WebInstagramClient.

Both clients use StdLoggingInstagramClientLogger by default, which routes
all output through Python's standard `logging` module under the logger name
"insta_wizard.client".

Three options depending on what you need:

  1. Default logger   — control verbosity via the standard logging API.
                        No changes to the client required.

  2. Custom logger    — pass your own logger=... to the client constructor.
                        Useful to integrate with structlog, loguru, etc.

  3. Silent (no logs) — pass NoOpInstagramClientLogger() to disable output.
"""

import asyncio
import logging

from insta_wizard import (
    InstagramClientLogger,
    MobileInstagramClient,
    NoOpInstagramClientLogger,
    WebInstagramClient,
)
from insta_wizard.common.transport.models import TransportResponse


# =============================================================================
# Option 1 — default logger
#
# No logger= argument needed. The client writes to "insta_wizard.client"
# via stdlib logging. Set the level to control what you see
# =============================================================================

logging.basicConfig(level=logging.INFO)
logging.getLogger("insta_wizard.client").setLevel(logging.DEBUG)


async def option_1_default_logger() -> None:
    # No logger= passed — StdLoggingInstagramClientLogger is used automatically.
    async with MobileInstagramClient() as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")
        await client.account.get_current_user()


# =============================================================================
# Option 2 — custom logger
#
# Subclass InstagramClientLogger and pass it via logger=.
# The same instance can be shared across multiple clients.
# =============================================================================

class MyLogger(InstagramClientLogger):
    def info(self, msg: object, *args, **kwargs) -> None:
        print(f"[INFO]  {msg % args if args else msg}")

    def error(self, msg: object, *args, **kwargs) -> None:
        print(f"[ERROR] {msg % args if args else msg}")

    def debug(self, msg: object, *args, **kwargs) -> None:
        pass  # suppress debug output

    def warning(self, msg: object, *args, **kwargs) -> None:
        print(f"[WARN]  {msg % args if args else msg}")

    def request(self, msg: object, *args, **kwargs) -> None:
        print(f"[-->]   {msg % args if args else msg}")

    def response(self, resp: TransportResponse, body: str | dict | None) -> None:
        print(f"[<--]   HTTP {resp.status} {resp.url}")


async def option_2_custom_logger() -> None:
    logger = MyLogger()

    async with MobileInstagramClient(logger=logger) as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")
        await client.account.get_current_user()

    # The same logger instance works with WebInstagramClient too.
    async with WebInstagramClient(logger=logger) as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")
        await client.account.get_edit_form_data()


# =============================================================================
# Option 3 — no logging
#
# Pass NoOpInstagramClientLogger() to suppress all client output entirely.
# =============================================================================

async def option_3_no_logging() -> None:
    async with MobileInstagramClient(logger=NoOpInstagramClientLogger()) as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")
        await client.account.get_current_user()


async def main() -> None:
    await option_1_default_logger()
    await option_2_custom_logger()
    await option_3_no_logging()


if __name__ == "__main__":
    asyncio.run(main())
