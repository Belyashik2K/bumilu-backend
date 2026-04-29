from pydantic import BaseModel

from app.modules.stats.presentation.api.schemas.places import PlacesStatsSchema
from app.modules.stats.presentation.api.schemas.routes import RoutesStatsSchema
from app.modules.stats.presentation.api.schemas.users import UsersStatsSchema


class GetDashboardStatsResponseSchema(BaseModel):
    users: UsersStatsSchema
    places: PlacesStatsSchema
    routes: RoutesStatsSchema
