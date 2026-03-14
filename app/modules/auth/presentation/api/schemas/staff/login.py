from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from app.modules.staff.presentation.api.schemas.common import (
    STAFF_MEMBER_EMAIL_EXAMPLE,
    STAFF_MEMBER_PASSWORD_EXAMPLE,
)


class StaffMemberLoginRequestSchema(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Email address of the staff member account.",
        examples=[STAFF_MEMBER_EMAIL_EXAMPLE],
    )
    password: str = Field(
        ...,
        description="Password for the staff member account.",
        examples=[STAFF_MEMBER_PASSWORD_EXAMPLE],
    )
