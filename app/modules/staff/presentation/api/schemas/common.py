from pydantic import (
    UUID7,
    BaseModel,
    EmailStr,
    Field,
)

from app.modules.staff.shared.enums.staff_role import StaffRoleEnum

STAFF_MEMBER_ID_EXAMPLE = "019caaaa-0000-7000-a000-000000001984"
STAFF_MEMBER_EMAIL_EXAMPLE = "belyashik2k@dev.bumilu.ru"
STAFF_MEMBER_PASSWORD_EXAMPLE = "supersecretpassword123"


class StaffMemberInfoSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier for the staff member.",
        examples=[STAFF_MEMBER_ID_EXAMPLE],
    )
    email: EmailStr = Field(
        ...,
        description="Email address of the staff member.",
        examples=[STAFF_MEMBER_EMAIL_EXAMPLE],
    )
    role: StaffRoleEnum = Field(
        ..., description="Role of the staff member.", examples=[StaffRoleEnum.OWNER]
    )


class AuthenticatedStaffMemberInfoSchema(StaffMemberInfoSchema): ...
