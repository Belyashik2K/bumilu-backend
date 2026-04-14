from app.core.application.queries import IQueryHandler
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.queries.places.admin.get_working_day_by_weekday.query import (
    GetAdminPlaceWorkingDayByWeekdayQuery,
)
from app.modules.places.application.queries.places.shared.models.place_working_day import (
    PlaceWorkingDayReadModel,
)


class GetAdminPlaceWorkingDayByWeekdayQueryHandler(
    IQueryHandler[GetAdminPlaceWorkingDayByWeekdayQuery, PlaceWorkingDayReadModel]
):
    def __init__(
        self,
        place_reader: IPlaceReader,
    ) -> None:
        self._place_reader = place_reader

    async def handle(
        self, query: GetAdminPlaceWorkingDayByWeekdayQuery
    ) -> PlaceWorkingDayReadModel:
        return await self._place_reader.get_working_day_by_weekday(
            place_id=query.place_id, weekday=query.weekday
        )
