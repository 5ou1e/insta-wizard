"""
Proxy usage — works with both MobileInstagramClient and WebInstagramClient.

Pass a ProxyInfo via the `proxy` constructor parameter and every request
will go through that proxy. You can also switch the proxy at runtime with
client.set_proxy().

For automatic proxy rotation on network errors see proxy_rotation.py.
"""

import asyncio

from insta_wizard import MobileInstagramClient, ProxyInfo
from insta_wizard.mobile.exceptions import NetworkError, TooManyRequestsError


# ---------------------------------------------------------------------------
# Building a ProxyInfo
# ---------------------------------------------------------------------------

# From individual fields:
proxy_from_fields = ProxyInfo(
    host="1.2.3.4",
    port=8080,
    username="user",  # optional
    password="pass",  # optional
)

# From a connection string — several formats are supported:
#   host:port
#   user:pass@host:port
#   http://user:pass@host:port
#   host:port:user:pass
proxy = ProxyInfo.from_string("http://user:pass@1.2.3.4:8080")


async def main() -> None:
    async with MobileInstagramClient(proxy=proxy) as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")

        user_id = "123456789"
        # --- Rotate proxy on NetworkError ------------------------------------
        try:
            await client.users.get_info(user_id)
        except NetworkError:
            # Proxy went down — switch and retry once.
            await client.set_proxy(ProxyInfo.from_string("5.6.7.8:8080:user2:pass2"))
            await client.users.get_info(user_id)

        # --- Rotate proxy on TooManyRequestsError ----------------------------
        try:
            await client.users.get_info(user_id)
        except TooManyRequestsError:
            # Instagram rate-limited the current IP — switch and retry once.
            await client.set_proxy(ProxyInfo.from_string("9.10.11.12:8080:user3:pass3"))
            await client.users.get_info(user_id)


if __name__ == "__main__":
    asyncio.run(main())
