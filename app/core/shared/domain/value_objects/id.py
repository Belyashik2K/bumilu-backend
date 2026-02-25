from dataclasses import (
    dataclass,
)
from typing import (
    Self,
)
from uuid import UUID

from uuid6 import (
    uuid7,
)


@dataclass(frozen=True, slots=True)
class IdVO:
    value: UUID

    @classmethod
    def new(cls) -> Self:
        return cls(uuid7())

    @classmethod
    def from_uuid(cls, uuid: UUID) -> Self:
        return cls(uuid)

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class SessionIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class DeviceIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class UserIdVO(IdVO): ...
