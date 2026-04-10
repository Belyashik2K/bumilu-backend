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
from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.staff.deps import get_staff_principal
from app.modules.auth.shared.context import Principal
from app.modules.places.application.commands.places.create.command import (
    CreatePlaceCommand,
)
from app.modules.places.application.commands.places.create.handler import (
    CreatePlaceCommandHandler,
)
from app.modules.places.application.commands.places.delete.command import (
    DeletePlaceCommand,
)
from app.modules.places.application.commands.places.delete.handler import (
    DeletePlaceCommandHandler,
)
from app.modules.places.application.commands.places.update.command import (
    UpdatePlaceCommand,
)
from app.modules.places.application.commands.places.update.handler import (
    UpdatePlaceCommandHandler,
)
from app.modules.places.presentation.api.schemas.places.main import (
    CreatePlaceRequestSchema,
    CreatePlaceResponseSchema,
    UpdatePlaceRequestSchema,
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
