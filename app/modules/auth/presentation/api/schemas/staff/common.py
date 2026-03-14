from pydantic import Field

from app.modules.auth.presentation.api.schemas.common import (
    AuthenticatedAccountInfoSchema,
    SuccessfulLoginSchema,
    TokenInfoSchema,
)


class SuccessfulStaffMemberLoginSchema(SuccessfulLoginSchema):
    refresh: TokenInfoSchema = Field(exclude=True)
    account: AuthenticatedAccountInfoSchema = Field(
        ...,
        description="Authenticated staff member information.",
        serialization_alias="staff_member",
    )
