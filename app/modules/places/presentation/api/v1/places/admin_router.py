from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)
from starlette import status

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
from app.modules.places.presentation.api.schemas.places.main import (
    CreatePlaceRequestSchema,
    CreatePlaceResponseSchema,
)

admin_places_router = APIRouter(
    prefix="/admin/places",
    tags=["Admin Places"],
    dependencies=[Depends(security)],
)


@admin_places_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses=generate_responses_for_endpoint(),
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
