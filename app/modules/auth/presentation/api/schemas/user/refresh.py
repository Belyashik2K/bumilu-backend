from app.modules.auth.presentation.api.schemas.user.login import (
    SuccessfulUserLoginSchema,
)


class RefreshUserAuthSessionResponseSchema(SuccessfulUserLoginSchema): ...
