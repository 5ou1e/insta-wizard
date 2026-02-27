from insta_wizard.common.models.checkpoint import (
    Checkpoint,
    UfacCheckpoint,
    UnknownCheckpoint,
    UfacStep,
    VettedDeltaCheckpoint,
    ScrapingWarningCheckpoint,
)
from insta_wizard.common.utils import iter_strings
from insta_wizard.web.commands import ChallengeWeb, BloksNavigationTakeChallenge
from insta_wizard.web.commands.challenge.challenge_web_action import ChallengeWebAction
from insta_wizard.web.exceptions import ResponseParsingError
from insta_wizard.web.models.other import CheckpointRequiredErrorData
from insta_wizard.web.sections.api import BaseSection
import re


class ChallengeSection(BaseSection):
    async def get_challenge_info(
        self, challenge_required_data: CheckpointRequiredErrorData
    ) -> Checkpoint:
        """Get checkpoint info"""

        challenge_info = await self.bus.execute(ChallengeWeb())
        self.logger.debug(f"Challenge info: {challenge_info}")
        return self.determine_checkpoint_by_url(
            url=challenge_required_data.checkpoint_url,
            challenge_info=challenge_info,
        )

    def determine_checkpoint_by_url(self, url: str, challenge_info: dict) -> Checkpoint:
        challenge_type = challenge_info.get("challengeType")
        if challenge_type == "ReviewLoginForm":
            return VettedDeltaCheckpoint()
        if challenge_type == "ScrapingWarningForm":
            return ScrapingWarningCheckpoint()

        # if challenge_type == "UFACWWWBloksScreen":
        #     return UfacCheckpoint()

        # Определяем сразу по url
        if "https://www.instagram.com/accounts/suspended/" in url:
            return UfacCheckpoint()
        if "https://www.instagram.com/accounts/disabled/" in url:
            return UfacCheckpoint(step=UfacStep.DISABLED)

        return UnknownCheckpoint(response=challenge_info)

    async def pass_vetted_delta(self, choice: str = "0") -> None:
        """Pass vetted_delta (delta_login_review) checkpoint

        :param choice: 0 - it was me, 1 - it was not me, 2 - close,
        """

        await self.bus.execute(
            ChallengeWebAction(
                choice=choice,
                next=None,
            )
        )

    async def pass_scraping_warning(self) -> None:
        """Pass scraping_warning checkpoint"""

        # Todo здесь надо принимать контекст, полученный через get_challenge_info, чтобы не повторять запрос
        challenge_info = await self.bus.execute(ChallengeWeb())
        challenge = self.determine_checkpoint_by_url(
            url="",
            challenge_info=challenge_info,
        )
        if not isinstance(challenge, ScrapingWarningCheckpoint):
            raise ValueError(f"Not scraping warning challenge: {challenge}")

        challenge_context = extract_challenge_context_for_scraping(data=challenge_info)

        await self.bus.execute(
            BloksNavigationTakeChallenge(
                challenge_context=challenge_context,
                has_follow_up_screens="false",
                nest_data_manifest="true",
            )
        )


def extract_challenge_context_for_scraping(data: dict):
    SUB = "com.instagram.challenge.navigation.take_challenge"

    hits = [s for s in iter_strings(data) if SUB in s]
    target_string = hits[0] if hits else None

    if target_string is not None:
        pattern = r'\\\"((?:\\.|[^\\]){200,})\\\"|"((?:\\.|[^"\\]){200,})"'
        m = re.search(pattern, target_string)
        challenge_context = (m.group(1) or m.group(2)) if m else None
        if challenge_context:
            return challenge_context

    raise ResponseParsingError(msg=f"Не удалось спарсить challenge_context из ответа")
