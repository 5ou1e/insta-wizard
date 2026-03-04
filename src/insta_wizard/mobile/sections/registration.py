from insta_wizard.common.interfaces import PhoneSmsCodeProvider
from insta_wizard.mobile.flows import RegisterAccountSMSFlow
from insta_wizard.mobile.flows.register_account_sms import CreatedUser
from insta_wizard.mobile.sections.api import BaseSection


class RegistrationSection(BaseSection):
    async def register_account_sms(
        self,
        username: str,
        password: str,
        first_name: str,
        day: int,
        month: int,
        year: int,
        phone_code_provider: PhoneSmsCodeProvider,
    ) -> CreatedUser:
        """Register an account using the code from the SMS"""

        return await self.bus.execute(
            RegisterAccountSMSFlow(
                username=username,
                password=password,
                first_name=first_name,
                day=day,
                month=month,
                year=year,
                phone_code_provider=phone_code_provider,
            )
        )
