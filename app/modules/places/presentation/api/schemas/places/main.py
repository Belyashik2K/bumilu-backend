from pydantic import (
    UUID7,
    BaseModel,
    Field,
)

from app.modules.places.presentation.api.schemas.places.address import (
    PlaceAddressSchema,
)
from app.modules.places.presentation.api.schemas.places.location import (
    PlaceLocationSchema,
)
from app.modules.places.presentation.api.schemas.places.phone import PlacePhoneSchema
from app.modules.places.presentation.api.schemas.places.working_hours import (
    END_TIME_EXAMPLE,
    START_TIME_EXAMPLE,
    PlaceWorkingHoursIntervalSchema,
)

UUID_EXAMPLE = "123e4567-e89b-12d3-a456-426614174000"
TITLE_EXAMPLE = 'Massage parlor "У Димасика"'
DESCRIPTION_EXAMPLE = "A cozy massage parlor located in the Vyborgsky district of St. Petersburg, offering a variety of massage services to help you relax and rejuvenate. Our experienced therapists use high-quality oils and techniques to provide a personalized massage experience tailored to your needs. Whether you're looking for a deep tissue massage, a relaxing Swedish massage, or a therapeutic sports massage, we have the perfect treatment for you. Visit us today and let us help you unwind and feel your best!"
SHORT_DESCRIPTION_EXAMPLE = "A cozy massage parlor located in the Vyborgsky district of St. Petersburg, offering a variety of massage services to help you relax and rejuvenate."
TIMEZONE_EXAMPLE = "Europe/Moscow"


class PlaceSchema(BaseModel):
    id: UUID7 = Field(
        ...,
        description="Unique identifier of the place",
        examples=[UUID_EXAMPLE],
    )
    category_id: UUID7 = Field(
        ...,
        description="Unique identifier of the place category",
        examples=[UUID_EXAMPLE],
    )
    title: str = Field(
        ...,
        description="Title of the place",
        examples=[TITLE_EXAMPLE],
    )
    description: str | None = Field(
        None,
        description="Description of the place",
        examples=[DESCRIPTION_EXAMPLE],
    )
    short_description: str | None = Field(
        None,
        description="Short description of the place",
        examples=[SHORT_DESCRIPTION_EXAMPLE],
    )
    timezone: str = Field(
        ...,
        description="Timezone of the place",
        examples=[TIMEZONE_EXAMPLE],
    )
    address: PlaceAddressSchema = Field(
        ...,
        description="Address of the place",
    )
    location: PlaceLocationSchema = Field(
        ...,
        description="Location of the place",
    )
    phones: list[PlacePhoneSchema] = Field(
        default_factory=list,
        description="List of place phones",
    )
    weekly_working_hours: dict[str, list[PlaceWorkingHoursIntervalSchema]] = Field(
        default_factory=dict,
        description=(
            "Weekly working hours represented as a dictionary where the key is the day of the week "
            "(1 for Monday, 7 for Sunday) and the value is a list of working hours intervals for that day."
        ),
        examples=[
            {
                "1": [
                    {"start": START_TIME_EXAMPLE, "end": END_TIME_EXAMPLE},
                ],
                "2": [
                    {"start": START_TIME_EXAMPLE, "end": END_TIME_EXAMPLE},
                ],
                "3": [
                    {"start": START_TIME_EXAMPLE, "end": END_TIME_EXAMPLE},
                ],
                "4": [
                    {"start": START_TIME_EXAMPLE, "end": END_TIME_EXAMPLE},
                ],
                "5": [
                    {"start": START_TIME_EXAMPLE, "end": END_TIME_EXAMPLE},
                ],
                "6": [
                    {"start": START_TIME_EXAMPLE, "end": END_TIME_EXAMPLE},
                ],
                "7": [
                    {"start": START_TIME_EXAMPLE, "end": END_TIME_EXAMPLE},
                ],
            }
        ],
    )
