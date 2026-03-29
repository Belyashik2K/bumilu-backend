from dataclasses import (
    dataclass,
    field,
)
from typing import Self


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetPaginationMixin:
    limit: int = field(default=20)
    offset: int = field(default=0)


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetPagination:
    limit: int
    offset: int
    total: int
    next_offset: int | None = field(default=None)
    prev_offset: int | None = field(default=None)

    @classmethod
    def create(cls, limit: int, offset: int, total: int) -> Self:
        next_offset = offset + limit if offset + limit < total else None
        prev_offset = max(offset - limit, 0) if offset > 0 else None

        return cls(
            limit=limit,
            offset=offset,
            total=total,
            next_offset=next_offset,
            prev_offset=prev_offset,
        )
