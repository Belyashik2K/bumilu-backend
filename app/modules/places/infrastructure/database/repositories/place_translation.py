from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.domain.value_objects.id import (
    PlaceIdVO,
    PlaceTranslationIdVO,
)
from app.core.enums import LanguageEnum
from app.core.infrastructure.database import SQLAlchemyBaseRepository
from app.modules.places.application.interfaces.repositories.place_translation import (
    IPlaceTranslationRepository,
)
from app.modules.places.domain.places.models.place_translation.model import (
    PlaceTranslation,
    PlaceTranslationData,
)
from app.modules.places.domain.places.value_objects.description.object import (
    PlaceDescriptionVO,
)
from app.modules.places.domain.places.value_objects.display_address.object import (
    PlaceDisplayAddressVO,
)
from app.modules.places.domain.places.value_objects.short_description.object import (
    PlaceShortDescriptionVO,
)
from app.modules.places.domain.places.value_objects.title.object import PlaceTitleVO
from app.modules.places.infrastructure.database.models import PlaceTranslationModel


class SQLAlchemyPlaceTranslationRepository(
    IPlaceTranslationRepository,
    SQLAlchemyBaseRepository[PlaceTranslation, PlaceTranslationModel],
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model_class=PlaceTranslationModel)

    def _to_data(self, entity: PlaceTranslation) -> PlaceTranslationModel:
        return PlaceTranslationModel(
            id=entity.id.value,
            place_id=entity.place_id.value,
            language_code=entity.data.language_code,
            title=entity.data.title.value,
            description=entity.data.description.value,
            short_description=entity.data.short_description.value,
            address_display=entity.data.display_address.value,
        )

    def _to_entity(self, model: PlaceTranslationModel) -> PlaceTranslation:
        return PlaceTranslation(
            id=PlaceTranslationIdVO.from_uuid(model.id),
            place_id=PlaceIdVO.from_uuid(model.place_id),
            data=PlaceTranslationData(
                language_code=model.language_code,
                title=PlaceTitleVO(model.title),
                description=PlaceDescriptionVO(model.description),
                short_description=PlaceShortDescriptionVO(model.short_description),
                display_address=PlaceDisplayAddressVO(model.address_display),
            ),
        )

    async def get_by_place_id_and_language_code(
        self, place_id: PlaceIdVO, language_code: LanguageEnum
    ) -> PlaceTranslation | None:
        stmt = select(PlaceTranslationModel).where(
            PlaceTranslationModel.place_id == place_id.value,
            PlaceTranslationModel.language_code == language_code.value,
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_entity(model)

    async def delete_by_id(self, translation_id: PlaceTranslationIdVO) -> None:
        stmt = delete(PlaceTranslationModel).where(
            PlaceTranslationModel.id == translation_id.value
        )
        await self.session.execute(stmt)
        await self.session.flush()
