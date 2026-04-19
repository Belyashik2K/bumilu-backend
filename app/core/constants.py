class UnsetType:
    __slots__ = ()

    def __repr__(self) -> str:
        return "UNSET"


UNSET = UnsetType()


def is_unset(value: object) -> bool:
    return value is UNSET
