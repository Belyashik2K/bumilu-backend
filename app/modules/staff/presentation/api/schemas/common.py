from datetime import datetime

from pydantic import (
    UUID7,
    BaseModel,
    EmailStr,
    Field,
)

from app.core.presentation.api.schemas.pagination import make_paginated_response_schema
from app.modules.staff.shared.enums.staff_role import StaffRoleEnum

STAFF_MEMBER_NAME_EXAMPLE = "Dmitrii Sokolov"
STAFF_MEMBER_ID_EXAMPLE = "019caaaa-0000-7000-a000-000000001984"
STAFF_MEMBER_EMAIL_EXAMPLE = "belyashik2k@dev.bumilu.ru"
STAFF_MEMBER_PASSWORD_EXAMPLE = "supersecretpassword123"


class CreateStaffMemberRequestSchema(BaseModel):
    name: str = Field(
        ...,
        description="Full name of the staff member.",
        examples=[STAFF_MEMBER_NAME_EXAMPLE],
    )
    email: EmailStr = Field(
        ...,
        description="Email address of the staff member.",
        examples=[STAFF_MEMBER_EMAIL_EXAMPLE],
    )
    password: str = Field(
        ...,
        description="Password for the staff member's account.",
        examples=[STAFF_MEMBER_PASSWORD_EXAMPLE],
    )
    role: StaffRoleEnum = Field(
        ..., description="Role of the staff member.", examples=[StaffRoleEnum.ADMIN]
    )


class StaffMemberInfoSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier for the staff member.",
        examples=[STAFF_MEMBER_ID_EXAMPLE],
    )
    name: str = Field(
        ...,
        description="Full name of the staff member.",
        examples=[STAFF_MEMBER_NAME_EXAMPLE],
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


class FullStaffMemberInfoSchema(AuthenticatedStaffMemberInfoSchema):
    created_at: datetime = Field(
        ...,
        description="Timestamp when the staff member was created.",
    )


PaginatedFullStaffMemberInfoSchema = make_paginated_response_schema(
    item_type=FullStaffMemberInfoSchema,
    description="Paginated list of staff members with full information.",
)
