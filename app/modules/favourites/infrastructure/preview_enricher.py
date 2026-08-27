from collections.abc import Mapping
from typing import cast
from uuid import UUID

from app.core.enums import LanguageEnum
from app.modules.favourites.application.interfaces.preview_enricher import (
    IFavouritePreviewEnricher,
)
from app.modules.favourites.application.interfaces.preview_provider import (
    IFavouritePreviewProvider,
)
from app.modules.favourites.application.queries.shared.models.favourite_entity import (
    FavouriteEntityReadModel,
)
from app.modules.favourites.application.queries.shared.models.favourite_record import (
    FavouriteRecordReadModel,
    RawFavouriteRecordReadModel,
)
from app.modules.favourites.shared.enums import FavouriteEntityTypeEnum
from app.modules.places.application.queries.places.shared.views import PlaceCardView


class FavouritePreviewEnricher(IFavouritePreviewEnricher):
    def __init__(
        self,
        providers: list[IFavouritePreviewProvider],
    ) -> None:
        self._providers_by_type = {
            provider.supported_type: provider for provider in providers
        }

    async def enrich(
        self,
        items: list[RawFavouriteRecordReadModel],
        translation_language: LanguageEnum,
    ) -> list[FavouriteRecordReadModel]:
        ids_by_type: dict[FavouriteEntityTypeEnum, list[UUID]] = {}

        for item in items:
            ids_by_type.setdefault(item.entity.type, []).append(item.entity.id)

        previews_by_type: dict[FavouriteEntityTypeEnum, Mapping[UUID, object]] = {}

        for entity_type, ids in ids_by_type.items():
            provider = self._providers_by_type.get(entity_type)
            if not provider:
                previews_by_type[entity_type] = {}
                continue

            unique_ids = list(dict.fromkeys(ids))
            previews_by_type[entity_type] = await provider.load_many(
                unique_ids,
                translation_language=translation_language,
            )

        return [
            FavouriteRecordReadModel(
                entity=FavouriteEntityReadModel(
                    id=item.entity.id,
                    type=item.entity.type,
                    # TODO: preview is generic (object) at the provider interface level;
                    # only Place is currently favouritable, so this cast is safe for now.
                    preview=cast(
                        PlaceCardView,
                        previews_by_type.get(item.entity.type, {}).get(item.entity.id),
                    ),
                ),
                created_at=item.created_at,
            )
            for item in items
        ]
