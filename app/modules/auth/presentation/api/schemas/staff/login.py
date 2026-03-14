from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

STAFF_EMAIL_EXAMPLE = "belyashik2k@dev.bumilu.ru"
STAFF_PASSWORD_EXAMPLE = "supersecretpassword123"


class StaffMemberLoginRequestSchema(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Email address of the staff member account.",
        examples=[STAFF_EMAIL_EXAMPLE],
    )
    password: str = Field(
        ...,
        description="Password for the staff member account.",
        examples=[STAFF_PASSWORD_EXAMPLE],
    )
