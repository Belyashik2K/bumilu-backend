from pydantic import (
    BaseModel,
    Field,
)


class OffsetPaginationQuery(BaseModel):
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Number of items to return",
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Number of items to skip",
    )


class OffsetPaginationSchema(BaseModel):
    limit: int = Field(
        ...,
        description="The maximum number of items to be returned in the response.",
        examples=[20],
    )
    offset: int = Field(
        ...,
        description="The number of items to skip before starting to collect the result set.",
        examples=[0],
    )
    total: int = Field(
        ...,
        description="The total number of items available in the data source.",
        examples=[100],
    )
    next_offset: int | None = Field(
        None,
        description="The offset value for the next page of results, or null if there are no more pages.",
        examples=[20],
    )
    prev_offset: int | None = Field(
        None,
        description="The offset value for the previous page of results, or null if there are no previous pages.",
        examples=[0],
    )
