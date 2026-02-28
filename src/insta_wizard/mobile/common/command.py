from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast

if TYPE_CHECKING:
    from insta_wizard.mobile.models.deps import ClientDeps

R = TypeVar("R")
C = TypeVar("C", bound="Command[Any]")


class Command(Generic[R]):
    pass


class CommandHandler(Generic[C, R]):
    async def __call__(self, command: C) -> R:
        raise NotImplementedError


HandlerFactory = Callable[[Any], CommandHandler[Any, Any]]


class CommandBus:
    def __init__(self, factories: Mapping[type[Any], HandlerFactory]) -> None:
        self._deps: ClientDeps | None = None
        self._factories: Mapping[type[Any], HandlerFactory] = factories

    def bind_deps(self, deps: ClientDeps) -> None:
        self._deps = deps

    async def execute(self, command: Command[R]) -> R:
        if self._deps is None:
            raise RuntimeError("CommandBus: client-deps not bound yet")

        cmd_type = type(command)

        factory = self._factories.get(cmd_type)
        if factory is None:
            raise KeyError(f"Command handler not found for {cmd_type.__name__}")

        handler = factory(self._deps)
        return await cast(Any, handler)(command)
