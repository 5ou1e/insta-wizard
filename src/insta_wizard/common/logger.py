import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from insta_wizard.common.transport.models import TransportResponse

LOGGER_NAME = "insta_wizard.client"
logging.getLogger(LOGGER_NAME).addHandler(logging.NullHandler())


class InstagramClientLogger(ABC):
    @abstractmethod
    def info(self, msg: object, *args: Any, **kwargs: Any) -> None: ...
    @abstractmethod
    def error(self, msg: object, *args: Any, **kwargs: Any) -> None: ...
    @abstractmethod
    def debug(self, msg: object, *args: Any, **kwargs: Any) -> None: ...
    @abstractmethod
    def warning(self, msg: object, *args: Any, **kwargs: Any) -> None: ...
    @abstractmethod
    def request(self, msg: object, *args: Any, **kwargs: Any) -> None: ...
    @abstractmethod
    def response(self, resp: "TransportResponse", body: str | dict | None) -> None: ...


class NoOpInstagramClientLogger(InstagramClientLogger):
    def info(self, msg: object, *args: Any, **kwargs: Any) -> None: ...
    def error(self, msg: object, *args: Any, **kwargs: Any) -> None: ...
    def debug(self, msg: object, *args: Any, **kwargs: Any) -> None: ...
    def warning(self, msg: object, *args: Any, **kwargs: Any) -> None: ...
    def request(self, msg: object, *args: Any, **kwargs: Any) -> None: ...
    def response(self, resp: "TransportResponse", body: str | dict | None) -> None: ...


class StdLoggingInstagramClientLogger(InstagramClientLogger):
    def __init__(
        self,
        logger: logging.Logger | None = None,
        log_request: bool = True,
        log_response: bool = True,
    ) -> None:
        self._logger = logger or logging.getLogger(LOGGER_NAME)
        self._log_request = log_request
        self._log_response = log_response

    def info(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self._logger.info(msg, *args, **kwargs)

    def error(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self._logger.error(msg, *args, **kwargs)

    def debug(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self._logger.debug(msg, *args, **kwargs)

    def warning(self, msg: object, *args: Any, **kwargs: Any) -> None:
        self._logger.warning(msg, *args, **kwargs)

    def request(self, msg: object, *args: Any, **kwargs: Any) -> None:
        if not self._log_request:
            return
        self._logger.info(msg, *args, **kwargs)

    def response(self, resp: "TransportResponse", body: str | dict | None) -> None:
        if not self._log_response:
            return
        if not self._logger.isEnabledFor(logging.INFO):
            return

        headers_str = "\n".join(f"  {k}: {v}" for k, v in resp.headers.items())
        safe_body = str(body) if body is not None else "<empty>"

        self._logger.info(
            "Response\nStatus: %s\nHTTP: %s\nHeaders:\n%s\nBody:\n  %s",
            resp.status,
            resp.http_version or "<unknown>",
            headers_str or "  <empty>",
            safe_body,
        )
