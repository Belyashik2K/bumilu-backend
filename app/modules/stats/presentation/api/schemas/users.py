from pydantic import (
    BaseModel,
    Field,
)


class UsersStatsSchema(BaseModel):
    total: int = Field(
        ...,
        description="The total number of users in the system",
    )
