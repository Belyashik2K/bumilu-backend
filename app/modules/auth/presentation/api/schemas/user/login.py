from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from app.modules.auth.presentation.api.schemas.common import (
    AuthenticatedAccountInfoSchema,
    SuccessfulLoginSchema,
)
from app.modules.users.presentation.api.schemas.common import USER_EMAIL_EXAMPLE

VERIFICATION_CODE_EXAMPLE = "123456"


class SuccessfulUserLoginSchema(SuccessfulLoginSchema):
    account: AuthenticatedAccountInfoSchema = Field(
        serialization_alias="user",
        description="Authenticated user's account information.",
    )


class RequestEmailCodeAtLoginRequestSchema(BaseModel):
    email: EmailStr = Field(
        ..., description="User's email address.", examples=[USER_EMAIL_EXAMPLE]
    )


class VerifyEmailCodeAtLoginRequestSchema(BaseModel):
    email: EmailStr = Field(
        ..., description="User's email address.", examples=[USER_EMAIL_EXAMPLE]
    )
    code: str = Field(
        ...,
        description="Verification code sent to the user's email.",
        examples=[VERIFICATION_CODE_EXAMPLE],
    )
