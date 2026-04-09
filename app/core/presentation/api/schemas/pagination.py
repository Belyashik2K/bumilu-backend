from typing import (
    Annotated,
    Generic,
    TypeVar,
)

from fastapi import Query
from fastapi.params import Depends
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

MINIMUM_LIMIT = 1
MAXIMUM_LIMIT = 100

MINIMUM_OFFSET = 0

DEFAULT_LIMIT = 20
DEFAULT_OFFSET = 0

TOTAL_EXAMPLE = 100
NEXT_OFFSET_EXAMPLE = 20
PREV_OFFSET_EXAMPLE = 0

T = TypeVar("T")


class OffsetPaginationQuery(BaseModel):
    limit: int = Field(
        DEFAULT_LIMIT,
        ge=MINIMUM_LIMIT,
        le=MAXIMUM_LIMIT,
        description="Number of items to return",
    )
    offset: int = Field(
        DEFAULT_OFFSET,
        ge=MINIMUM_OFFSET,
        description="Number of items to skip",
    )


class OffsetPaginationSchema(BaseModel):
    limit: int = Field(
        ...,
        description="The maximum number of items to be returned in the response.",
        examples=[DEFAULT_LIMIT],
    )
    offset: int = Field(
        ...,
        description="The number of items to skip before starting to collect the result set.",
        examples=[DEFAULT_OFFSET],
    )
    total: int = Field(
        ...,
        description="The total number of items available in the data source.",
        examples=[TOTAL_EXAMPLE],
    )
    next_offset: int | None = Field(
        None,
        description="The offset value for the next page of results, or null if there are no more pages.",
        examples=[NEXT_OFFSET_EXAMPLE],
    )
    prev_offset: int | None = Field(
        None,
        description="The offset value for the previous page of results, or null if there are no previous pages.",
        examples=[PREV_OFFSET_EXAMPLE],
    )


def get_offset_pagination(
    limit: Annotated[
        int,
        Query(
            ge=MINIMUM_LIMIT,
            le=MAXIMUM_LIMIT,
            description="Number of items to return",
        ),
    ] = DEFAULT_LIMIT,
    offset: Annotated[
        int,
        Query(
            ge=MINIMUM_OFFSET,
            description="Number of items to skip",
        ),
    ] = DEFAULT_OFFSET,
) -> OffsetPaginationQuery:
    return OffsetPaginationQuery(limit=limit, offset=offset)


class BasePaginatedResponseSchema(BaseModel, Generic[T]):
    model_config = ConfigDict(populate_by_name=True)

    data: list[T] = Field(
        ...,
        description="Dynamic field containing the list of items. The name of this field is determined by the 'json_key' parameter when creating the schema.",
    )
    pagination: OffsetPaginationSchema = Field(
        ...,
        description="Pagination metadata.",
    )


# TODO: Replace all manually defined paginated response schemas with dynamically generated ones using this function
def make_paginated_response_schema(
    item_type: type[T],
    *,
    description: str | None = None,
    serialization_alias: str | None = None,
    validation_alias: str | None = None,
) -> type[BasePaginatedResponseSchema[T]]:
    model_name = f"Paginated{item_type.__name__.rstrip("Schema")}ResponseSchema"

    class ConcretePaginatedResponseSchema(BasePaginatedResponseSchema[item_type]):  # type: ignore
        model_config = ConfigDict(
            title=model_name,
            validate_by_name=True,
            validate_by_alias=True,
        )

        data: list[item_type] = Field(  # type: ignore
            ...,
            description=description or f"List of {item_type.__name__} items.",
            serialization_alias=serialization_alias,
            validation_alias=validation_alias,
        )

    ConcretePaginatedResponseSchema.__name__ = model_name
    ConcretePaginatedResponseSchema.__qualname__ = model_name
    ConcretePaginatedResponseSchema.model_rebuild(force=True)

    return ConcretePaginatedResponseSchema


OffsetPaginationDep = Annotated[OffsetPaginationQuery, Depends(get_offset_pagination)]
