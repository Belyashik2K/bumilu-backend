from pydantic import (
    UUID7,
    BaseModel,
    EmailStr,
    Field,
)

from app.core.shared.enums import UserRoleEnum

DEVICE_ID_EXAMPLE = "019c95e5-f659-7698-a7dd-7738003a7d23"
USER_EMAIL_EXAMPLE = "belyashik2k@dev.bumilu.ru"
USER_ROLE_EXAMPLE = UserRoleEnum.GUEST


class UserInfoSchema(BaseModel):
    id: UUID7 = Field(
        ..., description="Unique identifier for the user.", examples=[DEVICE_ID_EXAMPLE]
    )
    email: EmailStr | None = Field(
        None, description="Email address of the user.", examples=[USER_EMAIL_EXAMPLE]
    )
    role: UserRoleEnum = Field(
        ..., description="Role of the user.", examples=[USER_ROLE_EXAMPLE]
    )


class AuthenticatedUserInfoSchema(UserInfoSchema): ...
