from fastapi.params import Header
from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.shared.enums import DevicePlatformEnum

DEVICE_ID_EXAMPLE = "019caaaa-0000-7000-a000-000000000001"
DEVICE_PLATFORM_EXAMPLE = DevicePlatformEnum.ANDROID
DEVICE_NAME_EXAMPLE = "Xiaomi 11T (Android 11)"
APP_VERSION_EXAMPLE = "1.0.0"


class DeviceInfoHeadersSchema(BaseModel):
    device_id: UUID7 = Field(
        ...,
        description="Unique identifier for the device.",
        examples=[DEVICE_ID_EXAMPLE],
    )
    device_platform: DevicePlatformEnum = Field(
        ...,
        description="Platform of the device.",
        examples=[DEVICE_PLATFORM_EXAMPLE],
    )
    device_name: str | None = Field(
        None,
        description="Name of the device.",
        examples=[DEVICE_NAME_EXAMPLE],
    )
    app_version: str = Field(
        ..., description="Version of the app.", examples=[APP_VERSION_EXAMPLE]
    )


def get_device_info_headers(
    device_id: UUID7 = Header(  # type: ignore
        ...,
        alias="X-Device-Id",
        description="Unique identifier for the device.",
        example=DEVICE_ID_EXAMPLE,
    ),
    device_platform: DevicePlatformEnum = Header(  # type: ignore
        ...,
        alias="X-Device-Platform",
        description="Platform of the device.",
        example=DEVICE_PLATFORM_EXAMPLE,
    ),
    device_name: str | None = Header(  # type: ignore
        None,
        alias="X-Device-Name",
        description="Name of the device.",
        example=DEVICE_NAME_EXAMPLE,
    ),
    app_version: str = Header(  # type: ignore
        ...,
        alias="X-App-Version",
        description="Version of the app.",
        example=APP_VERSION_EXAMPLE,
    ),
) -> DeviceInfoHeadersSchema:
    return DeviceInfoHeadersSchema(
        device_id=device_id,
        device_platform=device_platform,
        device_name=device_name,
        app_version=app_version,
    )
