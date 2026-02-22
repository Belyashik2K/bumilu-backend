from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.shared.enums import (
    DevicePlatformEnum,
)
from app.modules.auth.presentation.api.schemas.common import (
    DEVICE_ID_EXAMPLE,
    SuccessfulLoginSchema,
)


class LoginAsGuestRequestSchema(BaseModel):
    device_id: UUID7 = Field(
        ...,
        description="Unique identifier for the device.",
        examples=[DEVICE_ID_EXAMPLE],
    )
    device_platform: DevicePlatformEnum = Field(
        ...,
        description="Platform of the device.",
        examples=[DevicePlatformEnum.ANDROID],
    )
    device_name: str | None = Field(
        None,
        description="Name of the device.",
        examples=["Pixel 9 Pro (Android 14)"],
    )
    app_version: str = Field(..., description="Version of the app.", examples=["1.0.0"])


class LoginAsGuestResponseSchema(SuccessfulLoginSchema): ...
