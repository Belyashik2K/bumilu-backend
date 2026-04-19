from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Generic,
    Self,
    TypeVar,
)

T = TypeVar("T")


@dataclass(frozen=True, slots=True, kw_only=True)
class PageReadModel(Generic[T]):
    items: list[T] = field(default_factory=list)
    total: int = field(default=0)


@dataclass(frozen=True, kw_only=True)
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


@dataclass(frozen=True, slots=True, kw_only=True)
class DataListView(Generic[T]):
    data: list[T]

    @classmethod
    def create(cls, items: list[T]) -> Self:
        return cls(data=items)


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginatedView(Generic[T]):
    data: list[T]
    pagination: OffsetPagination

    @classmethod
    def create(cls, items: list[T], limit: int, offset: int, total: int) -> Self:
        pagination = OffsetPagination.create(limit=limit, offset=offset, total=total)
        return cls(data=items, pagination=pagination)
