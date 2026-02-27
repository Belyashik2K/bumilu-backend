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

    def __post_init__(self) -> None:
        if not isinstance(self.value, UUID):
            print(
                f"Invalid type for IdVO.value: expected UUID, got {type(self.value)!r}"
            )
            raise TypeError(f"IdVO.value must be UUID, got {type(self.value)!r}")

    @classmethod
    def new(cls) -> Self:
        return cls(uuid7())

    @classmethod
    def from_uuid(cls, uuid: UUID) -> Self:
        return cls(UUID(str(uuid)))  # TODO: remove redundant conversion once

    @classmethod
    def from_str(cls, uuid_str: str) -> Self:
        return cls(UUID(uuid_str))

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class SessionIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class DeviceIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class UserIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class ReviewIdVO(IdVO): ...
