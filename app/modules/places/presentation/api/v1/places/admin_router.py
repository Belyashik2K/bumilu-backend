from typing import (
    Annotated,
)

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import UUID7
from starlette import status

from app.core.application.queries.pagination import (
    DataListView,
    PaginatedView,
)
from app.core.constants import UNSET
from app.core.enums import LanguageEnum
from app.core.presentation.api.schemas.accept_language import (
    AcceptLanguageDep,
)
from app.core.presentation.api.schemas.bbox import BBoxDep
from app.core.presentation.api.schemas.pagination import OffsetPaginationDep
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
from app.modules.places.application.commands.places.change_status.command import (
    ChangePlaceStatusCommand,
)
from app.modules.places.application.commands.places.change_status.handler import (
    ChangePlaceStatusCommandHandler,
)
from app.modules.places.application.commands.places.complete_photo_upload.command import (
    CompletePlacePhotoUploadCommand,
)
from app.modules.places.application.commands.places.complete_photo_upload.handler import (
    CompletePlacePhotoUploadCommandHandler,
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
from app.modules.places.application.commands.places.delete_photo.command import (
    DeletePlacePhotoCommand,
)
from app.modules.places.application.commands.places.delete_photo.handler import (
    DeletePlacePhotoCommandHandler,
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
from app.modules.places.application.commands.places.replace_working_day.command import (
    ReplacePlaceWorkingDayCommand,
    WorkingDayIntervalData,
)
from app.modules.places.application.commands.places.replace_working_day.handler import (
    ReplacePlaceWorkingDayCommandHandler,
)
from app.modules.places.application.commands.places.start_photo_upload.command import (
    StartPlacePhotoUploadCommand,
)
from app.modules.places.application.commands.places.start_photo_upload.handler import (
    StartPlacePhotoUploadCommandHandler,
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
from app.modules.places.application.queries.places.admin.get.handler import (
    GetAdminPlaceQueryHandler,
)
from app.modules.places.application.queries.places.admin.get.query import (
    GetAdminPlaceQuery,
)
from app.modules.places.application.queries.places.admin.get_all.handler import (
    GetAdminPlacesListQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_all.query import (
    GetAdminPlacesListQuery,
)
from app.modules.places.application.queries.places.admin.get_map_poi.handler import (
    GetAdminPlacesMapPOIQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_map_poi.query import (
    GetAdminPlacesMapPOIQuery,
)
from app.modules.places.application.queries.places.admin.get_phones.handler import (
    GetAdminPlacePhonesQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_phones.query import (
    GetAdminPlacePhonesQuery,
)
from app.modules.places.application.queries.places.admin.get_photos.handler import (
    GetAdminPlacePhotosQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_photos.query import (
    GetAdminPlacePhotosQuery,
)
from app.modules.places.application.queries.places.admin.get_photos.view import (
    AdminPlacePhotoView,
)
from app.modules.places.application.queries.places.admin.get_translation_by_language_code.handler import (
    GetAdminPlaceTranslationByLanguageCodeQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_translation_by_language_code.query import (
    GetAdminPlaceTranslationByLanguageCodeQuery,
)
from app.modules.places.application.queries.places.admin.get_translations.handler import (
    GetAdminPlaceTranslationsQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_translations.query import (
    GetAdminPlaceTranslationsQuery,
)
from app.modules.places.application.queries.places.admin.get_working_day_by_weekday.handler import (
    GetAdminPlaceWorkingDayByWeekdayQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_working_day_by_weekday.query import (
    GetAdminPlaceWorkingDayByWeekdayQuery,
)
from app.modules.places.application.queries.places.admin.get_working_days.handler import (
    GetAdminPlaceWorkingDaysQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_working_days.query import (
    GetAdminPlaceWorkingDaysQuery,
)
from app.modules.places.application.queries.places.shared.dtos import BBox
from app.modules.places.application.queries.places.shared.models.place_card import (
    AdminPlaceCardReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_details import (
    AdminPlaceDetailsReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_map_poi import (
    AdminPlaceMapPOIReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_phone import (
    AdminPlacePhoneReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_translation import (
    PlaceTranslationReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_working_day import (
    PlaceWorkingDayReadModel,
)
from app.modules.places.presentation.api.schemas.places.main import (
    ChangePlaceStatusRequestSchema,
    CreatePlaceRequestSchema,
    CreatePlaceResponseSchema,
    UpdatePlaceRequestSchema,
)
from app.modules.places.presentation.api.schemas.places.phone import (
    PlacePhoneSchema,
    UpdatePlacePhoneSchema,
)
from app.modules.places.presentation.api.schemas.places.photo import (
    StartPlacePhotoUploadRequestSchema,
    StartPlacePhotoUploadResponseSchema,
)
from app.modules.places.presentation.api.schemas.places.translation import (
    CreatePlaceTranslationRequestSchema,
    UpdatePlaceTranslationRequestSchema,
)
from app.modules.places.presentation.api.schemas.places.working_day import (
    ReplacePlaceWorkingDaySchema,
)

admin_places_router = APIRouter(
    prefix="/admin/places",
    tags=["Admin Places"],
    dependencies=[Depends(security)],
)


@admin_places_router.get(
    "/map/pois",
    responses=generate_responses_for_endpoint(status.HTTP_404_NOT_FOUND),
)
@inject
async def list_places_map_pois(
    handler: FromDishka[GetAdminPlacesMapPOIQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    bound: BBoxDep,
    accept_language: AcceptLanguageDep,
) -> DataListView[AdminPlaceMapPOIReadModel]:
    result = await handler(
        GetAdminPlacesMapPOIQuery(
            bounds=BBox(
                south=bound.south,
                west=bound.west,
                north=bound.north,
                east=bound.east,
            ),
            language=accept_language.language,
        )
    )
    return result


@admin_places_router.get(
    "",
    responses=generate_responses_for_endpoint(status.HTTP_404_NOT_FOUND),
)
@inject
async def list_places(
    handler: FromDishka[GetAdminPlacesListQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    accept_language: AcceptLanguageDep,
    pagination: OffsetPaginationDep,
    title_like: str | None = None,
    category_slug: str | None = None,
) -> PaginatedView[AdminPlaceCardReadModel]:
    result = await handler(
        GetAdminPlacesListQuery(
            title_like=title_like,
            category_slug=category_slug,
            limit=pagination.limit,
            offset=pagination.offset,
            language=accept_language.language,
        )
    )
    return result


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


@admin_places_router.get(
    "/{place_id}",
    responses=generate_responses_for_endpoint(status.HTTP_404_NOT_FOUND),
)
@inject
async def get_place_details(
    place_id: UUID7,
    handler: FromDishka[GetAdminPlaceQueryHandler],
    accept_language: AcceptLanguageDep,
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> AdminPlaceDetailsReadModel:
    result = await handler(
        GetAdminPlaceQuery(
            place_id=place_id,
            language=accept_language.language,
        )
    )
    return result


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


@admin_places_router.patch(
    "/{place_id}/status",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def change_place_status(
    place_id: UUID7,
    handler: FromDishka[ChangePlaceStatusCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: ChangePlaceStatusRequestSchema,
) -> None:
    await handler(
        ChangePlaceStatusCommand(
            place_id=place_id,
            status=data.status,
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


@admin_places_router.get(
    "/{place_id}/translations",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def list_place_translations(
    place_id: UUID7,
    handler: FromDishka[GetAdminPlaceTranslationsQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> PaginatedView[PlaceTranslationReadModel]:
    result = await handler(
        GetAdminPlaceTranslationsQuery(
            place_id=place_id,
        )
    )
    return result


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


@admin_places_router.get(
    "/{place_id}/translations/{language_code}",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def get_place_translation(
    place_id: UUID7,
    language_code: LanguageEnum,
    handler: FromDishka[GetAdminPlaceTranslationByLanguageCodeQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> PlaceTranslationReadModel:
    result = await handler(
        GetAdminPlaceTranslationByLanguageCodeQuery(
            place_id=place_id,
            language_code=language_code,
        )
    )
    return result


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


@admin_places_router.get(
    "/{place_id}/phones",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def list_place_phones(
    place_id: UUID7,
    handler: FromDishka[GetAdminPlacePhonesQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> DataListView[AdminPlacePhoneReadModel]:
    result = await handler(
        GetAdminPlacePhonesQuery(
            place_id=place_id,
        )
    )
    return result


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


@admin_places_router.get(
    "/{place_id}/working-days",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def get_place_working_days(
    place_id: UUID7,
    handler: FromDishka[GetAdminPlaceWorkingDaysQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> DataListView[PlaceWorkingDayReadModel]:
    result = await handler(
        GetAdminPlaceWorkingDaysQuery(
            place_id=place_id,
        )
    )
    return result


@admin_places_router.get(
    "/{place_id}/working-days/{weekday}",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def get_place_working_day_by_weekday(
    place_id: UUID7,
    weekday: int,
    handler: FromDishka[GetAdminPlaceWorkingDayByWeekdayQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> PlaceWorkingDayReadModel:
    result = await handler(
        GetAdminPlaceWorkingDayByWeekdayQuery(
            place_id=place_id,
            weekday=weekday,
        )
    )
    return result


@admin_places_router.put(
    "/{place_id}/working-days/{weekday}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def replace_place_working_day(
    place_id: UUID7,
    weekday: int,
    handler: FromDishka[ReplacePlaceWorkingDayCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: ReplacePlaceWorkingDaySchema,
) -> None:
    await handler(
        ReplacePlaceWorkingDayCommand(
            place_id=place_id,
            weekday=weekday,
            status=data.status,
            intervals=[
                WorkingDayIntervalData(start_time=interval.start, end_time=interval.end)
                for interval in data.intervals
            ],
        )
    )


@admin_places_router.get(
    "/{place_id}/photos",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
    ),
)
@inject
async def list_place_photos(
    place_id: UUID7,
    handler: FromDishka[GetAdminPlacePhotosQueryHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> DataListView[AdminPlacePhotoView]:
    result = await handler(
        GetAdminPlacePhotosQuery(
            place_id=place_id,
        )
    )
    return result


@admin_places_router.post(
    "/{place_id}/photos/upload",
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def start_place_photo_upload(
    place_id: UUID7,
    handler: FromDishka[StartPlacePhotoUploadCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
    data: StartPlacePhotoUploadRequestSchema,
) -> StartPlacePhotoUploadResponseSchema:
    result = await handler(
        StartPlacePhotoUploadCommand(
            place_id=place_id,
            content_type=data.content_type,
        )
    )
    return StartPlacePhotoUploadResponseSchema.model_validate(
        result, from_attributes=True
    )


@admin_places_router.post(
    "/{place_id}/photos/{photo_id}/complete",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def complete_place_photo_upload(
    place_id: UUID7,
    photo_id: UUID7,
    handler: FromDishka[CompletePlacePhotoUploadCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> None:
    await handler(
        CompletePlacePhotoUploadCommand(
            place_id=place_id,
            photo_id=photo_id,
        )
    )


@admin_places_router.delete(
    "/{place_id}/photos/{photo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=generate_responses_for_endpoint(
        status.HTTP_404_NOT_FOUND,
        status.HTTP_409_CONFLICT,
    ),
)
@inject
async def delete_place_photo(
    place_id: UUID7,
    photo_id: UUID7,
    handler: FromDishka[DeletePlacePhotoCommandHandler],
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> None:
    await handler(
        DeletePlacePhotoCommand(
            place_id=place_id,
            photo_id=photo_id,
        )
    )
