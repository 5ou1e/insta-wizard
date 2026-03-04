"""
Mobile client — account registration via SMS.

The registration flow:
  1. Provide a phone number
  2. Instagram sends an SMS with a 6-digit code
  3. Submit the code to verify the number
  4. Create the account (username, password, name, birthday)

PhoneSmsCodeProvider
--------------------
The flow requires a PhoneSmsCodeProvider — an object with two async methods:

    provide_number() -> str   # returns the phone number, e.g. "+12025550100"
    provide_code()   -> str   # waits for the SMS and returns the code, e.g. "123456"

Two provider implementations are shown below:

  ManualPhoneSmsCodeProvider  — built-in, asks via input() (for manual testing)
  CustomSmsServiceProvider    — your own implementation of PhoneSmsCodeProvider for interacting SMS-activation service or something else

"""

import asyncio
import json
import random
import secrets
import string

from insta_wizard import MobileInstagramClient
from insta_wizard.common.interfaces import ManualPhoneSmsCodeProvider, PhoneSmsCodeProvider

STATE_FILE = "new_account_state.json"


# ---------------------------------------------------------------------------
# Option B: custom provider — plug in any SMS-activation API here
# ---------------------------------------------------------------------------
class CustomSmsServiceProvider(PhoneSmsCodeProvider):
    async def provide_number(self, new: bool = False) -> str:
        # Call your SMS service API to rent a number and return it.
        # Example: return await my_sms_api.get_number()
        raise NotImplementedError("Implement SMS service integration here")

    async def provide_code(self) -> str:
        # Poll your SMS service API until the code arrives, then return it.
        # Example: return await my_sms_api.get_code()
        raise NotImplementedError("Implement SMS service integration here")


# Helper — generate random account credentials
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

    # Option A: interactive — asks for number and code via input()
    provider = ManualPhoneSmsCodeProvider()

    # Option B: automated SMS service (uncomment and implement CustomSmsServiceProvider)
    # provider = CustomSmsServiceProvider()

    async with MobileInstagramClient() as client:
        created_user = await client.registration.register_account_sms(
            phone_code_provider=provider,
            **creds,
        )

        print(
            f"Account created!"
            f"\ncreated_user={created_user}"
        )

        # Save the full client state so the session can be resumed later.
        state = client.dump_state()
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
        print(f"Session state saved to {STATE_FILE!r}")


if __name__ == "__main__":
    asyncio.run(main())
