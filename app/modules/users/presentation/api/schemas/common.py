from pydantic import (
    UUID7,
    BaseModel,
    EmailStr,
    Field,
)

from app.core.shared.enums import UserRoleEnum

USER_ID_EXAMPLE = "019caaaa-0000-7000-a000-000000001984"
USER_EMAIL_EXAMPLE = "belyashik2k@dev.bumilu.ru"
USER_ROLE_EXAMPLE = UserRoleEnum.USER


class UserInfoSchema(BaseModel):
    id: UUID7 = Field(
        ..., description="Unique identifier for the user.", examples=[USER_ID_EXAMPLE]
    )
    email: EmailStr | None = Field(
        None, description="Email address of the user.", examples=[USER_EMAIL_EXAMPLE]
    )
    role: UserRoleEnum = Field(
        ..., description="Role of the user.", examples=[USER_ROLE_EXAMPLE]
    )


class AuthenticatedUserInfoSchema(UserInfoSchema): ...
