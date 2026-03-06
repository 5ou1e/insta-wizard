from insta_wizard.common.interfaces import EmailCodeSignupProvider, PhoneSmsCodeProvider
from insta_wizard.mobile.flows import RegisterAccountSMSFlow
from insta_wizard.mobile.flows.register_account_email import RegisterAccountEmailFlow, RegisterAccountEmailFlowResult
from insta_wizard.mobile.flows.register_account_sms import RegisterAccountSMSFlowResult
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
    ) -> RegisterAccountSMSFlowResult:
        """Register an account via SMS (phone number)"""

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

    async def register_account_email(
        self,
        username: str,
        password: str,
        first_name: str,
        day: int,
        month: int,
        year: int,
        email_code_provider: EmailCodeSignupProvider,
    ) -> RegisterAccountEmailFlowResult:
        """Register an account via Email"""

        return await self.bus.execute(
            RegisterAccountEmailFlow(
                username=username,
                password=password,
                first_name=first_name,
                day=day,
                month=month,
                year=year,
                email_code_provider=email_code_provider,
            )
        )
