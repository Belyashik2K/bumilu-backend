from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.core.presentation.api.schemas.pagination import make_data_list_response_schema
from app.modules.places.presentation.api.schemas.places.examples import (
    PHOTO_THUMBNAIL_URL_EXAMPLE,
    PHOTO_URL_EXAMPLE,
    UUID_EXAMPLE,
)
from app.modules.places.shared.enums.place_photo_status import PlacePhotoStatusEnum


class PlacePhotoSchema(BaseModel):
    url: str = Field(
        ...,
        description="The URL of the photo.",
        examples=[PHOTO_URL_EXAMPLE],
    )
    thumbnail_url: str | None = Field(
        None,
        description="The URL of the thumbnail version of the photo.",
        examples=[PHOTO_THUMBNAIL_URL_EXAMPLE],
    )


class AdminPlacePhotoSchema(PlacePhotoSchema):
    id: UUID7 = Field(
        ...,
        description="The unique identifier of the photo.",
        examples=[UUID_EXAMPLE],
    )
    status: PlacePhotoStatusEnum = Field(
        ...,
        description="The status of the photo.",
        examples=[PlacePhotoStatusEnum.READY],
    )


class StartPlacePhotoUploadRequestSchema(BaseModel):
    content_type: str = Field(
        ..., description="The MIME type of the photo.", examples=["image/jpeg"]
    )


class StartPlacePhotoUploadResponseSchema(BaseModel):
    photo_id: UUID7 = Field(
        ...,
        description="The unique identifier of the photo.",
        examples=[UUID_EXAMPLE],
    )
    file_key: str = Field(
        ...,
        description="The key under which the photo will be stored in the file storage.",
        examples=[
            "places/123e4567-e89b-12d3-a456-426614174000/photos/123e4567-e89b-12d3-a456-426614174001/original.jpg"
        ],
    )
    upload_url: str = Field(
        ...,
        description="The URL to which the photo should be uploaded.",
        examples=[PHOTO_URL_EXAMPLE],
    )
    expires_in: int = Field(
        ...,
        description="The number of seconds until the upload URL expires.",
        examples=[3600],
    )


AdminPlacePhotoListResponseSchema = make_data_list_response_schema(
    item_type=AdminPlacePhotoSchema,
    description="Response schema for a list of photos associated with a place, including administrative details.",
)
