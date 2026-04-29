from typing import Annotated

from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    Depends,
)

from app.core.presentation.endpoint_responses import generate_responses_for_endpoint
from app.modules.auth.presentation.api import security
from app.modules.auth.presentation.api.v1.staff.deps import get_staff_principal
from app.modules.auth.shared.context import Principal
from app.modules.stats.presentation.api.schemas.main import (
    GetDashboardStatsResponseSchema,
)
from app.modules.stats.presentation.api.schemas.places import PlacesStatsSchema
from app.modules.stats.presentation.api.schemas.routes import RoutesStatsSchema
from app.modules.stats.presentation.api.schemas.users import UsersStatsSchema

stats_router = APIRouter(
    tags=["Statistics"],
    dependencies=[Depends(security)],
)


@stats_router.get("/admin/dashboard/stats", responses=generate_responses_for_endpoint())
@inject
async def get_dashboard_stats(
    principal: Annotated[Principal, Depends(get_staff_principal)],
) -> GetDashboardStatsResponseSchema:
    result = GetDashboardStatsResponseSchema(
        places=PlacesStatsSchema(
            published=51,
            hidden=4,
            total=55,
        ),
        routes=RoutesStatsSchema(
            total=7,
        ),
        users=UsersStatsSchema(
            total=102,
        ),
    )
    return result
