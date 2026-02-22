from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)

from app.modules.auth.presentation.api.schemas.common import (
    DEVICE_ID_EXAMPLE,
    TOKEN_EXAMPLE,
    SuccessfulLoginSchema,
)


class RefreshAuthSessionRequestSchema(BaseModel):
    refresh_token: str = Field(
        ...,
        description="The refresh token issued during authentication or previous refresh.",
        examples=[TOKEN_EXAMPLE],
    )
    device_id: UUID = Field(
        ...,
        description="Unique identifier for the device.",
        examples=[DEVICE_ID_EXAMPLE],
    )


class RefreshAuthSessionResponseSchema(SuccessfulLoginSchema): ...
