from pydantic import (
    BaseModel,
    Field,
)


class PlacesStatsSchema(BaseModel):
    published: int = Field(
        ...,
        description="The number of published places in the system",
    )
    hidden: int = Field(
        ...,
        description="The number of hidden places in the system",
    )
    total: int = Field(
        ...,
        description="The total number of places in the system",
    )
