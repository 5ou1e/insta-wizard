import random

from insta_wizard.common.logger import InstagramClientLogger
from insta_wizard.common.models.checkpoint import (
    Checkpoint,
    ScrapingWarningCheckpoint,
    UfacCheckpoint,
    UnknownCheckpoint,
    VettedDeltaCheckpoint,
)
from insta_wizard.mobile.commands import ChallengeAction, ChallengeGetChallengeInfo
from insta_wizard.mobile.common.command import CommandBus
from insta_wizard.mobile.models.challenge import ChallengeRequiredData
from insta_wizard.mobile.models.state import MobileClientState
from insta_wizard.mobile.responses.challenge_info import ChallengeGetChallengeInfoResponse
from insta_wizard.mobile.sections.api import BaseSection
from insta_wizard.mobile.sections.graphql_www import GraphqlWWW


class ChallengeSection(BaseSection):
    def __init__(
        self,
        state: MobileClientState,
        bus: CommandBus,
        graphql_www: GraphqlWWW,
        logger: InstagramClientLogger,
    ):
        self.graphql_www = graphql_www
        self.logger = logger
        super().__init__(state=state, bus=bus)

    async def get_challenge_info(self, challenge_data: ChallengeRequiredData) -> Checkpoint | None:
        """Get challenge info
        Returns Checkpoint info object or None if no challenge
        """

        if not challenge_data.api_path:
            raise ValueError("Отсутствует api_path в challenge_data")

        challenge_info = await self.bus.execute(
            ChallengeGetChallengeInfo(
                api_path=challenge_data.api_path.lstrip("/"),
                challenge_context=challenge_data.challenge_context,
            )
        )
        # {'action': 'close', 'status': 'ok'}
        if challenge_info.get("action") == "close":
            return None

        self.logger.debug(f"Challenge info: {challenge_info}")

        # TODO это можно выполнять аналогично через https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.ig.challenge.redirect.async/
        challenge_bloks = await self.graphql_www.IGBloksAppRootQuery_challenge_redirect_async(
            challenge_context=challenge_info["challenge_context"]
        )
        self.logger.debug(f"Challenge bloks-info: {challenge_bloks}")

        return self.determine_checkpoint_by_challenge_info(
            challenge_info=challenge_info, challenge_bloks=challenge_bloks
        )

    def determine_checkpoint_by_challenge_info(
        self,
        challenge_info: ChallengeGetChallengeInfoResponse,
        challenge_bloks: dict,
    ) -> Checkpoint:
        challenge_type_enum_str = challenge_info.get("challenge_type_enum_str")
        step_name = challenge_info.get("step_name")

        if challenge_type_enum_str == "UFAC_WWW_BLOKS":
            return UfacCheckpoint()

        if challenge_type_enum_str == "VETTED_DELTA" and step_name == "delta_login_review":
            return VettedDeltaCheckpoint()

        if challenge_info.get("bloks_action") == "com.bloks.www.ig.challenge.redirect.async":
            # Предполагаем, что это scraping_warning, у него вроде нету challenge_type_enum_str
            # has_scraping, marker_id, instance_id = parse_scraping_warning(challenge_bloks)

            if "com.bloks.www.ig.challenge.scraping_warning.async" in str(challenge_bloks):
                return ScrapingWarningCheckpoint()

        return UnknownCheckpoint(response=challenge_bloks)

    async def pass_vetted_delta(self, choice: str = "0") -> None:
        """Pass vetted_delta (delta_login_review) checkpoint

        :param choice: 0 - it was me, 1 - it was not me, 2 - close,
        """

        await self.bus.execute(ChallengeAction(choice=choice))

    async def pass_scraping_warning(self) -> None:
        """Pass scraping_warning checkpoint"""

        # TODO тут надо подставлять реальные значения с пред. запросов
        marker_id, instance_id = 36707139, random.randint(28160300002, 28160400002)

        await self.graphql_www.IGBloksAppRootQuery_scraping_warning_dismiss(
            marker_id,
            instance_id,
        )
