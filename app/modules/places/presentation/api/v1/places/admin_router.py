from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import UUID7
from starlette import status

from app.core.constants import UNSET
from app.core.enums import LanguageEnum
from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.staff.deps import get_staff_principal
from app.modules.auth.shared.context import Principal
from app.modules.places.application.commands.places.add_phone.command import (
    AddPlacePhoneCommand,
)
from app.modules.places.application.commands.places.add_phone.handler import (
    AddPlacePhoneCommandHandler,
)
from app.modules.places.application.commands.places.create.command import (
    CreatePlaceCommand,
)
from app.modules.places.application.commands.places.create.handler import (
    CreatePlaceCommandHandler,
)
from app.modules.places.application.commands.places.create_translation.command import (
    CreatePlaceTranslationCommand,
    PlaceTranslationData,
)
from app.modules.places.application.commands.places.create_translation.handler import (
    CreatePlaceTranslationCommandHandler,
)
from app.modules.places.application.commands.places.delete.command import (
    DeletePlaceCommand,
)
from app.modules.places.application.commands.places.delete.handler import (
    DeletePlaceCommandHandler,
)
from app.modules.places.application.commands.places.delete_phone.command import (
    DeletePlacePhoneCommand,
)
from app.modules.places.application.commands.places.delete_phone.handler import (
    DeletePlacePhoneCommandHandler,
)
from app.modules.places.application.commands.places.delete_translation.command import (
    DeletePlaceTranslationCommandHandler,
)
from app.modules.places.application.commands.places.delete_translation.handler import (
    DeletePlaceTranslationCommand,
)
from app.modules.places.application.commands.places.make_phone_primary.command import (
    MakePlacePhonePrimaryCommand,
)
from app.modules.places.application.commands.places.make_phone_primary.handler import (
    MakePlacePhonePrimaryCommandHandler,
)
from app.modules.places.application.commands.places.update.command import (
    UpdatePlaceCommand,
)
from app.modules.places.application.commands.places.update.handler import (
    UpdatePlaceCommandHandler,
)
from app.modules.places.application.commands.places.update_phone.command import (
    UpdatePlacePhoneCommand,
)
from app.modules.places.application.commands.places.update_phone.handler import (
    UpdatePlacePhoneCommandHandler,
)
from app.modules.places.application.commands.places.update_translation.command import (
    UpdatePlaceTranslationCommand,
    UpdatePlaceTranslationData,
)
from app.modules.places.application.commands.places.update_translation.handler import (
    UpdatePlaceTranslationCommandHandler,
)
from app.modules.places.presentation.api.schemas.places.main import (
    CreatePlaceRequestSchema,
    CreatePlaceResponseSchema,
    UpdatePlaceRequestSchema,
)
from app.modules.places.presentation.api.schemas.places.phone import (
    PlacePhoneSchema,
    UpdatePlacePhoneSchema,
)
from app.modules.places.presentation.api.schemas.places.translation import (
    CreatePlaceTranslationRequestSchema,
    UpdatePlaceTranslationRequestSchema,
)

admin_places_router = APIRouter(
    prefix="/admin/places",
    tags=["Admin Places"],
    dependencies=[Depends(security)],
)


@admin_places_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses=generate_responses_for_endpoint(status.HTTP_404_NOT_FOUND),
)
@inject
async def create_place(
    handler: FromDishka[CreatePlaceCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: CreatePlaceRequestSchema,
) -> CreatePlaceResponseSchema:
    result = await handler(
        CreatePlaceCommand(
            category_slug=data.category_slug,
            latitude=data.location.latitude,
            longitude=data.location.longitude,
            address_taxi=data.address_taxi,
            address_taxi_comment=data.address_taxi_comment,
        )
    )
    return CreatePlaceResponseSchema.model_validate(result, from_attributes=True)


@admin_places_router.patch(
    "/{place_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def update_place(
    place_id: UUID7,
    handler: FromDishka[UpdatePlaceCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: UpdatePlaceRequestSchema,
) -> None:
    data_dump = data.model_dump(exclude_unset=True)
    location = data_dump.get("location", UNSET)
    await handler(
        UpdatePlaceCommand(
            place_id=place_id,
            category_slug=data_dump.get("category_slug", UNSET),
            latitude=location["latitude"] if location is not UNSET else UNSET,
            longitude=location["longitude"] if location is not UNSET else UNSET,
            address_taxi=data_dump.get("address_taxi", UNSET),
            address_taxi_comment=data_dump.get("address_taxi_comment", UNSET),
        )
    )


@admin_places_router.delete(
    "/{place_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def delete_place(
    place_id: UUID7,
    handler: FromDishka[DeletePlaceCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> None:
    await handler(
        DeletePlaceCommand(
            place_id=place_id,
        )
    )


@admin_places_router.post(
    "/{place_id}/translations",
    status_code=status.HTTP_201_CREATED,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def create_place_translation(
    place_id: UUID7,
    handler: FromDishka[CreatePlaceTranslationCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: CreatePlaceTranslationRequestSchema,
) -> None:
    await handler(
        CreatePlaceTranslationCommand(
            place_id=place_id,
            data=PlaceTranslationData(
                language_code=data.language_code,
                title=data.title,
                description=data.description,
                short_description=data.short_description,
                display_address=data.display_address,
            ),
        )
    )


@admin_places_router.patch(
    "/{place_id}/translations/{language_code}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def update_place_translation(
    place_id: UUID7,
    language_code: LanguageEnum,
    handler: FromDishka[UpdatePlaceTranslationCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: UpdatePlaceTranslationRequestSchema,
) -> None:
    data_dump = data.model_dump(exclude_unset=True)
    await handler(
        UpdatePlaceTranslationCommand(
            place_id=place_id,
            data=UpdatePlaceTranslationData(
                language_code=language_code,
                title=data_dump.get("title", UNSET),
                description=data_dump.get("description", UNSET),
                short_description=data_dump.get("short_description", UNSET),
                display_address=data_dump.get("display_address", UNSET),
            ),
        )
    )


@admin_places_router.delete(
    "/{place_id}/translations/{language_code}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def delete_place_translation(
    place_id: UUID7,
    language_code: LanguageEnum,
    handler: FromDishka[DeletePlaceTranslationCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> None:
    await handler(
        DeletePlaceTranslationCommand(
            place_id=place_id,
            language_code=language_code,
        )
    )


@admin_places_router.post(
    "/{place_id}/phones",
    status_code=status.HTTP_201_CREATED,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def add_place_phone(
    place_id: UUID7,
    handler: FromDishka[AddPlacePhoneCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: PlacePhoneSchema,
) -> None:
    await handler(
        AddPlacePhoneCommand(
            place_id=place_id,
            number=data.number,
            type=data.type,
            is_primary=data.primary,
        )
    )


@admin_places_router.patch(
    "/{place_id}/phones/{phone_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def update_place_phone(
    place_id: UUID7,
    phone_id: UUID7,
    handler: FromDishka[UpdatePlacePhoneCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: UpdatePlacePhoneSchema,
) -> None:
    data_dump = data.model_dump(exclude_unset=True)
    await handler(
        UpdatePlacePhoneCommand(
            place_id=place_id,
            phone_id=phone_id,
            number=data_dump.get("number", UNSET),
            type=data_dump.get("type", UNSET),
        )
    )


@admin_places_router.delete(
    "/{place_id}/phones/{phone_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def delete_place_phone(
    place_id: UUID7,
    phone_id: UUID7,
    handler: FromDishka[DeletePlacePhoneCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> None:
    await handler(
        DeletePlacePhoneCommand(
            place_id=place_id,
            phone_id=phone_id,
        )
    )


@admin_places_router.post(
    "/{place_id}/phones/{phone_id}/make-primary",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def make_place_phone_primary(
    place_id: UUID7,
    phone_id: UUID7,
    handler: FromDishka[MakePlacePhonePrimaryCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> None:
    await handler(
        MakePlacePhonePrimaryCommand(
            place_id=place_id,
            phone_id=phone_id,
        )
    )
