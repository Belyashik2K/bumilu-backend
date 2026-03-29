from dataclasses import dataclass
from typing import Self

from app.core.domain.value_objects.id import PrincipalIdVO
from app.modules.auth.shared.enums import PrincipalTypeEnum


@dataclass(slots=True, kw_only=True)
class Principal:
    id: PrincipalIdVO
    type: PrincipalTypeEnum

    @classmethod
    def create(cls, type: PrincipalTypeEnum) -> Self:
        return cls(
            id=PrincipalIdVO.new(),
            type=type,
        )
