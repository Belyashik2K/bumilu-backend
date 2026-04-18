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
class ReviewIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class ChatIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class ChatMessageIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class PrincipalIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class PlaceIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class PlaceTranslationIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class PlacePhoneIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class PlaceWorkingDayIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class PlacePhotoIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class PlaceCategoryIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class PlaceCategoryTranslationIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class RouteIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class RoutePointIdVO(IdVO): ...


@dataclass(frozen=True, slots=True)
class RouteTranslationIdVO(IdVO): ...
