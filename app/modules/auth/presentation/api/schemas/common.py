from pydantic import (
    UUID7,
    BaseModel,
    EmailStr,
    Field,
)

from app.core.shared.enums import UserRoleEnum
from app.modules.staff.shared.enums.staff_role import StaffRoleEnum
from app.modules.users.presentation.api.schemas.common import (
    USER_EMAIL_EXAMPLE,
    USER_ID_EXAMPLE,
    USER_ROLE_EXAMPLE,
)

TOKEN_EXAMPLE = "itsshowinglikeitstheendoftheworld"
TOKEN_EXPIRES_IN_EXAMPLE = 3600


class AuthenticatedAccountInfoSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier for the account.",
        examples=[USER_ID_EXAMPLE],
    )
    email: EmailStr | None = Field(
        None, description="Email address of the account.", examples=[USER_EMAIL_EXAMPLE]
    )
    role: UserRoleEnum | StaffRoleEnum = Field(
        ..., description="Role of the account.", examples=[USER_ROLE_EXAMPLE]
    )


class TokenInfoSchema(BaseModel):
    token: str = Field(..., description="Token string.", examples=[TOKEN_EXAMPLE])
    expires_in: int = Field(
        ...,
        description="Expiration time in seconds.",
        examples=[TOKEN_EXPIRES_IN_EXAMPLE],
    )


class SuccessfulLoginSchema(BaseModel):
    access: TokenInfoSchema = Field(..., description="Access token information.")
    refresh: TokenInfoSchema = Field(..., description="Refresh token information.")
    account: AuthenticatedAccountInfoSchema = Field(
        ..., description="Authenticated account information."
    )


class RefreshAuthSessionRequestSchema(BaseModel):
    refresh_token: str = Field(
        ...,
        description="The refresh token issued during authentication or previous refresh.",
        examples=[TOKEN_EXAMPLE],
    )
