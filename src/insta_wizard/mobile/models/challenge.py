from pydantic import BaseModel


class ChallengeRequiredData(BaseModel):
    url: str
    api_path: str
    hide_webview_header: bool
    lock: bool
    logout: bool
    native_flow: bool
    flow_render_type: int
    challenge_context: str | None = None


class FeedbackRequiredData(BaseModel):
    feedback_title: str | None = None
    feedback_url: str | None = None
