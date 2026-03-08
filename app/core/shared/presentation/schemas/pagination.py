from pydantic import (
    BaseModel,
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
