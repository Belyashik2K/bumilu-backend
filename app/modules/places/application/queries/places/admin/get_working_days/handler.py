from app.core.application.queries import IQueryHandler
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.queries.places.admin.get_working_days.query import (
    GetAdminPlaceWorkingDaysQuery,
)
from app.modules.places.application.queries.places.shared.models.place_working_day import (
    PlaceWorkingDayReadModel,
)


class GetAdminPlaceWorkingDaysQueryHandler(
    IQueryHandler[GetAdminPlaceWorkingDaysQuery, list[PlaceWorkingDayReadModel]]
):
    def __init__(self, place_reader: IPlaceReader) -> None:
        self._place_reader = place_reader

    async def handle(
        self, query: GetAdminPlaceWorkingDaysQuery
    ) -> list[PlaceWorkingDayReadModel]:
        return await self._place_reader.get_working_days_by_id(place_id=query.place_id)
