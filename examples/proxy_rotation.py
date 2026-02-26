"""
Automatic proxy rotation — works with both MobileInstagramClient and WebInstagramClient.

When the transport encounters a network error (timeout / connection failure)
during request execution, it works through the following sequence:

  1. Retry the same request up to `max_retries_on_network_errors` more times.
  2. If ALL retries are exhausted and `change_proxy_after_all_failed_attempts`
     is True, call proxy_provider.provide_new() to get a new proxy, switch to
     it, and repeat the whole retry cycle from step 1.
  3. Stop switching after `max_proxy_changes` proxy changes (None = unlimited).
  4. If all proxy changes are exhausted — a NetworkError is raised.

The static `proxy` parameter and rotation are independent: you can omit the
initial proxy and still have rotation enabled — the provider will be called
from the very first failure.

─── TransportSettings parameters ─────────────────────────────────────────────
  max_network_wait_time                    — request timeout in seconds
  max_retries_on_network_errors            — extra attempts per proxy before rotating
  delay_before_retries_on_network_errors   — pause (s) between retry attempts
  change_proxy_after_all_failed_attempts   — enable rotation after exhausted retries
  max_proxy_changes                        — max proxy switches (None = unlimited)
  proxy_provider                           — supplies the next proxy on rotation
"""

import asyncio

from insta_wizard import MobileInstagramClient, ProxyInfo, TransportSettings, WebInstagramClient
from insta_wizard.common.interfaces import ProxyProvider


class MyProxyProvider(ProxyProvider):
    """Returns proxies from a list one by one."""

    def __init__(self, proxies: list[str]) -> None:
        self._proxies = iter(ProxyInfo.from_string(p) for p in proxies)

    async def provide_new(self) -> ProxyInfo | None:
        return next(self._proxies, None)


def make_transport(provider: ProxyProvider) -> TransportSettings:
    return TransportSettings(
        max_network_wait_time=30,
        max_retries_on_network_errors=2,             # 2 extra attempts per proxy
        delay_before_retries_on_network_errors=1.0,  # 1 s between attempts
        change_proxy_after_all_failed_attempts=True,
        max_proxy_changes=5,
        proxy_provider=provider,
    )


async def mobile_example() -> None:
    provider = MyProxyProvider(["1.2.3.4:8080:u1:p1", "5.6.7.8:8080:u2:p2"])

    async with MobileInstagramClient(
        transport_settings=make_transport(provider),
        proxy=ProxyInfo.from_string("9.10.11.12:8080:u0:p0"),  # optional starting proxy
    ) as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")
        await client.account.get_current_user()


async def web_example() -> None:
    provider = MyProxyProvider(["1.2.3.4:8080:u1:p1", "5.6.7.8:8080:u2:p2"])

    async with WebInstagramClient(
        transport_settings=make_transport(provider),
        proxy=ProxyInfo.from_string("9.10.11.12:8080:u0:p0"),  # optional starting proxy
    ) as client:
        await client.login("YOUR_USERNAME", "YOUR_PASSWORD")
        await client.account.get_edit_form_data()


async def main() -> None:
    await mobile_example()
    await web_example()


if __name__ == "__main__":
    asyncio.run(main())
