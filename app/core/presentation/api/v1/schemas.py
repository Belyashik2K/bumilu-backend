from pydantic import (
    BaseModel,
    Field,
)


class HealthCheckResponse(BaseModel):
    status: str = Field(
        "ok",
        description="The status of the response"
    )
