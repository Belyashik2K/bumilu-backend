from dataclasses import (
    dataclass,
    field,
)
from typing import Self

from app.core.domain.value_objects.id import (
    PlaceCategoryIdVO,
)
from app.core.enums import LanguageEnum
from app.modules.places.domain.categories.models.category_translation.model import (
    NewPlaceCategoryTranslation,
    PlaceCategoryTranslation,
)
from app.modules.places.domain.categories.value_objects.icon_key import (
    PlaceCategoryIconKeyVO,
)
from app.modules.places.domain.categories.value_objects.marker_color.object import (
    PlaceCategoryMarkerColorVO,
)
from app.modules.places.domain.categories.value_objects.slug import PlaceCategorySlugVO


@dataclass(slots=True, kw_only=True)
class PlaceCategory:
    id: PlaceCategoryIdVO
    slug: PlaceCategorySlugVO
    icon_key: PlaceCategoryIconKeyVO
    marker_color: PlaceCategoryMarkerColorVO
    translation_language_codes: set[LanguageEnum] = field(default_factory=set)

    @classmethod
    def create(
        cls,
        slug: PlaceCategorySlugVO,
        icon_key: PlaceCategoryIconKeyVO,
        marker_color: PlaceCategoryMarkerColorVO,
        translations: list[NewPlaceCategoryTranslation],
    ) -> tuple[Self, list[PlaceCategoryTranslation]]:
        if not translations:
            raise ValueError("Place category must have at least one translation")

        category = PlaceCategory(
            id=PlaceCategoryIdVO.new(),
            slug=slug,
            icon_key=icon_key,
            marker_color=marker_color,
        )

        language_codes = [translation.language_code for translation in translations]
        if len(language_codes) != len(set(language_codes)):
            raise ValueError("Translation language codes must be unique")

        created_translations = [
            category.create_translation(data=translation)
            for translation in translations
        ]
        return category, created_translations

    def create_translation(
        self, data: NewPlaceCategoryTranslation
    ) -> PlaceCategoryTranslation:
        if data.language_code in self.translation_language_codes:
            raise ValueError(
                f"Translation for language {data.language_code} already exists"
            )

        translation = PlaceCategoryTranslation.create(
            category_id=self.id,
            data=data,
        )
        self.translation_language_codes.add(data.language_code)

        return translation
