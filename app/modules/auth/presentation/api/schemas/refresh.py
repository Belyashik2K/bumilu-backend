from pydantic import (
    BaseModel,
    Field,
)

from app.modules.auth.presentation.api.schemas.common import (
    TOKEN_EXAMPLE,
    SuccessfulLoginSchema,
)


class RefreshAuthSessionRequestSchema(BaseModel):
    refresh_token: str = Field(
        ...,
        description="The refresh token issued during authentication or previous refresh.",
        examples=[TOKEN_EXAMPLE],
    )


class RefreshAuthSessionResponseSchema(SuccessfulLoginSchema): ...
