from pydantic import (
    BaseModel,
    Field,
)


class RoutesStatsSchema(BaseModel):
    total: int = Field(
        ...,
        description="The total number of routes in the system",
    )
