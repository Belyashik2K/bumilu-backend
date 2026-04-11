from app.core.application.commands import ICommandHandler
from app.core.application.interfaces.transaction_manager import ITransactionManager
from app.core.domain.value_objects.id import PlaceIdVO
from app.modules.places.application.commands.places.replace_working_day.command import (
    ReplacePlaceWorkingDayCommand,
)
from app.modules.places.application.exceptions.place import PlaceNotFound
from app.modules.places.application.interfaces.repositories.place import (
    IPlaceRepository,
)
from app.modules.places.domain.places.models.place_working_day.model import (
    PlaceWorkingDayData,
)
from app.modules.places.domain.places.value_objects.weekday.object import WeekdayVO
from app.modules.places.domain.places.value_objects.working_interval.object import (
    WorkingIntervalVO,
)


class ReplacePlaceWorkingDayCommandHandler(
    ICommandHandler[ReplacePlaceWorkingDayCommand]
):
    def __init__(
        self,
        transaction_manager: ITransactionManager,
        place_repository: IPlaceRepository,
    ) -> None:
        super().__init__(transaction_manager)
        self._place_repository = place_repository

    async def handle(self, command: ReplacePlaceWorkingDayCommand) -> None:
        place_id = PlaceIdVO.from_uuid(command.place_id)
        place = await self._place_repository.get_by_id_with_working_days(place_id)
        if place is None:
            raise PlaceNotFound(place_id.value)

        place.replace_working_day(
            PlaceWorkingDayData(
                weekday=WeekdayVO(command.weekday),
                status=command.status,
                intervals=[
                    WorkingIntervalVO(
                        start_time=interval.start_time,
                        end_time=interval.end_time,
                    )
                    for interval in command.intervals
                ],
            )
        )

        await self._place_repository.save(place)
