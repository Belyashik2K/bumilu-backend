from pydantic import (
    UUID7,
    BaseModel,
    Field,
)
from uuid6 import uuid7

from app.core.shared.enums import UserRoleEnum

DEVICE_ID_EXAMPLE = uuid7()
EMAIL_EXAMPLE = "belyashik2k@bumilu.ru"
VERIFICATION_CODE_EXAMPLE = "123456"
TOKEN_EXAMPLE = "itsshowinglikeitstheendoftheworld"


class AuthenticatedUserInfoSchema(BaseModel):
    id: UUID7 = Field(
        ..., description="Unique identifier for the user.", examples=[DEVICE_ID_EXAMPLE]
    )
    role: UserRoleEnum = Field(
        ..., description="Role of the user.", examples=[UserRoleEnum.GUEST]
    )


class TokenInfoSchema(BaseModel):
    token: str = Field(..., description="Token string.", examples=[TOKEN_EXAMPLE])
    expires_in: int = Field(
        ..., description="Expiration time in seconds.", examples=[3600]
    )


class SuccessfulLoginSchema(BaseModel):
    access: TokenInfoSchema = Field(..., description="Access token information.")
    refresh: TokenInfoSchema = Field(..., description="Refresh token information.")
    user: AuthenticatedUserInfoSchema = Field(
        ..., description="Authenticated user information."
    )
