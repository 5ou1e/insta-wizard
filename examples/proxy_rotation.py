"""
Automatic proxy rotation — works with both MobileInstagramClient and WebInstagramClient.

When the transport encounters a network error (timeout / connection failure)
during request execution, it works through the following sequence:

  1. Retry the same request up to `network_error_retry_limit` more times.
  2. If ALL retries are exhausted and `change_proxies`
     is True, call proxy_provider.provide_new() to get a new proxy, switch to
     it, and repeat the whole retry cycle from step 1.
  3. Stop switching after `proxy_change_limit` proxy changes (None = unlimited).
  4. If all proxy changes are exhausted — a NetworkError is raised.

The static `proxy` parameter and rotation are independent: you can omit the
initial proxy and still have rotation enabled — the provider will be called
from the very first failure.

─── TransportSettings parameters ─────────────────────────────────────────────
  network_timeout          — request timeout in seconds
  network_error_retry_limit — extra attempts per proxy before rotating
  network_error_retry_delay — pause (s) between retry attempts
  change_proxies           — enable rotation after exhausted retries
  proxy_change_limit       — max proxy switches (None = unlimited)
  proxy_provider           — supplies the next proxy on rotation
"""

import asyncio

from insta_wizard import MobileInstagramClient, ProxyInfo, TransportSettings, WebInstagramClient
from insta_wizard.common.interfaces import ProxyProvider


class MyProxyProvider(ProxyProvider):
    """Returns proxies from a hardcoded list one by one."""

    _proxies = [
        "194.67.201.14:8080:user1:pass1",
        "91.108.4.220:3128:user2:pass2",
        "185.199.229.156:7492:user3:pass3",
        "45.142.212.10:31281:user4:pass4",
        "103.149.162.195:8080:user5:pass5",
    ]
    _index = 0

    async def provide_new(self) -> ProxyInfo | None:
        if self._index >= len(self._proxies):
            return None
        proxy = ProxyInfo.from_string(self._proxies[self._index])
        self._index += 1
        return proxy


def make_transport() -> TransportSettings:
    return TransportSettings(
        network_timeout=30,
        network_error_retry_limit=2,    # 2 extra attempts per proxy
        network_error_retry_delay=1.0,  # 1 s between attempts
        change_proxies=True,
        proxy_change_limit=5,
        proxy_provider=MyProxyProvider(),
    )


async def mobile_example() -> None:
    async with MobileInstagramClient(
        transport_settings=make_transport(),
        proxy=ProxyInfo.from_string("62.33.207.196:3128:user0:pass0"),  # optional starting proxy
    ) as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")
        await client.account.get_current_user()


async def web_example() -> None:
    async with WebInstagramClient(
        transport_settings=make_transport(),
        proxy=ProxyInfo.from_string("62.33.207.196:3128:user0:pass0"),  # optional starting proxy
    ) as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")
        await client.account.get_edit_form_data()


async def main() -> None:
    await mobile_example()
    await web_example()


if __name__ == "__main__":
    asyncio.run(main())
