from app.modules.places.application.queries.categories.shared.models.place_category import (
    LocalizedPlaceCategoryReadModel,
    PlaceCategoryReadModel,
)
from app.modules.places.infrastructure.database.models import PlaceCategoryModel


class PlaceCategoryMapper:
    @staticmethod
    def map_category(
        category: PlaceCategoryModel,
    ) -> PlaceCategoryReadModel:
        return PlaceCategoryReadModel(
            id=category.id,
            slug=category.slug,
            icon_key=category.icon_key,
            marker_color=category.marker_color,
        )

    @staticmethod
    def map_localized_category(
        category: PlaceCategoryModel,
    ) -> LocalizedPlaceCategoryReadModel:
        translation = category.translations[0]
        return LocalizedPlaceCategoryReadModel(
            id=category.id,
            slug=category.slug,
            name=translation.name,
            icon_key=category.icon_key,
            marker_color=category.marker_color,
        )
