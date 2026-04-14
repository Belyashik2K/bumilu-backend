from app.core.application.queries import IQueryHandler
from app.modules.places.application.interfaces.readers.place import IPlaceReader
from app.modules.places.application.queries.places.admin.get_phones.query import (
    GetAdminPlacePhonesQuery,
)
from app.modules.places.application.queries.places.shared.models.place_phone import (
    AdminPlacePhoneReadModel,
)


class GetAdminPlacePhonesQueryHandler(
    IQueryHandler[GetAdminPlacePhonesQuery, list[AdminPlacePhoneReadModel]]
):
    def __init__(
        self,
        place_reader: IPlaceReader,
    ) -> None:
        self._place_reader = place_reader

    async def handle(
        self, query: GetAdminPlacePhonesQuery
    ) -> list[AdminPlacePhoneReadModel]:
        return await self._place_reader.get_admin_phones_by_id(place_id=query.place_id)
