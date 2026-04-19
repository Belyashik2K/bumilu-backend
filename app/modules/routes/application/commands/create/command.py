from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateRouteCommand: ...


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateRouteCommandResult:
    id: UUID
