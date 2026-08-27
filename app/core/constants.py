from typing import TypeIs


class UnsetType:
    __slots__ = ()

    def __repr__(self) -> str:
        return "UNSET"


UNSET = UnsetType()


def is_unset(value: object) -> TypeIs[UnsetType]:
    return value is UNSET
