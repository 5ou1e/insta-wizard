"""
Mobile client — account registration via Email.

The registration flow:
  1. Provide an email address
  2. Instagram sends a 6-digit verification code to that email
  3. Submit the code to verify the address
  4. Create the account (username, password, name, birthday)

EmailCodeSignupProvider
-----------------------
The flow requires an EmailCodeSignupProvider — an object with two async methods:

    provide_email()                         -> str   # returns the email address, e.g. "user@example.com"
    provide_code(email, from_datetime)      -> str   # waits for the email and returns the code, e.g. "123456"

Two provider implementations are shown below:

  ManualEmailCodeSignupProvider  — built-in, asks via input() (for manual testing)
  CustomEmailServiceProvider     — your own implementation of EmailCodeSignupProvider for interacting
                                   with an email inbox API or a temporary-mail service

"""

import asyncio
import json
import random
import secrets
import string

from insta_wizard import MobileClient
from insta_wizard.common.interfaces import EmailCodeSignupProvider, ManualEmailCodeSignupProvider



# ---------------------------------------------------------------------------
# Custom provider — plug in any email / temp-mail API here
# ---------------------------------------------------------------------------
class CustomEmailServiceProvider(EmailCodeSignupProvider):
    async def provide_email(self) -> str:
        # Create / obtain a temporary email address and return it.
        # Example: return await my_mail_api.create_inbox()
        raise NotImplementedError()

    async def provide_code(self, email: str, from_datetime) -> str:
        # Poll your email service until the verification email arrives, then return the code.
        # Example: return await my_mail_api.wait_for_code(email, since=from_datetime)
        raise NotImplementedError()


# Generate random account credentials
def generate_registration_info() -> dict:
    username = "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(24))
    password = secrets.token_urlsafe(12) + "!"
    first_name = secrets.token_urlsafe(8).capitalize()
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1970, 2000)
    return dict(
        username=username,
        password=password,
        first_name=first_name,
        day=day,
        month=month,
        year=year,
    )


async def main() -> None:
    creds = generate_registration_info()
    print(f"Registration attempt with: username={creds['username']}, password={creds['password']}")

    provider = ManualEmailCodeSignupProvider() # or CustomEmailServiceProvider()

    async with MobileClient() as client:
        result = await client.registration.register_account_email(
            email_code_provider=provider,
            **creds,
        )

        print(
            f"Account created!"
            f"\ncreated_user={result.created_user}"
            f"\nemail={result.email}"
        )

        # Save the full client state so the session can be resumed later.
        state = client.dump_state()
        username = creds['username']
        with open(f"{username}.json", "w") as f:
            json.dump(state, f, indent=2)


if __name__ == "__main__":
    asyncio.run(main())
