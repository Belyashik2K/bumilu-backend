from dataclasses import (
    dataclass,
    field,
)
from typing import Self

from app.core.domain.value_objects.id import (
    PlaceCategoryIdVO,
)
from app.core.enums import LanguageEnum
from app.modules.places.domain.categories.models.category.exceptions import (
    CannotDeleteOnlyPlaceCategoryTranslation,
    DuplicatePlaceCategoryTranslationLanguageCodes,
    PlaceCategoryMustHaveAtLeastOneTranslation,
    PlaceCategoryTranslationAlreadyExists,
    PlaceCategoryTranslationNotFound,
)
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
            raise PlaceCategoryMustHaveAtLeastOneTranslation()

        category = PlaceCategory(
            id=PlaceCategoryIdVO.new(),
            slug=slug,
            icon_key=icon_key,
            marker_color=marker_color,
        )

        language_codes = [translation.language_code for translation in translations]
        if len(language_codes) != len(set(language_codes)):
            raise DuplicatePlaceCategoryTranslationLanguageCodes(
                language_codes=language_codes
            )

        created_translations = [
            category.create_translation(data=translation)
            for translation in translations
        ]
        return category, created_translations

    def update(
        self,
        *,
        slug: PlaceCategorySlugVO | None = None,
        icon_key: PlaceCategoryIconKeyVO | None = None,
        marker_color: PlaceCategoryMarkerColorVO | None = None,
    ) -> None:
        if slug is not None and slug != self.slug:
            self.slug = slug
        if icon_key is not None and icon_key != self.icon_key:
            self.icon_key = icon_key
        if marker_color is not None and marker_color != self.marker_color:
            self.marker_color = marker_color

    def create_translation(
        self, data: NewPlaceCategoryTranslation
    ) -> PlaceCategoryTranslation:
        if data.language_code in self.translation_language_codes:
            raise PlaceCategoryTranslationAlreadyExists(
                category_id=self.id,
                language_code=data.language_code,
            )

        translation = PlaceCategoryTranslation.create(
            category_id=self.id,
            data=data,
        )
        self.translation_language_codes.add(data.language_code)

        return translation

    def ensure_translation_can_be_deleted(self, language_code: LanguageEnum) -> None:
        if language_code not in self.translation_language_codes:
            raise PlaceCategoryTranslationNotFound(
                category_id=self.id,
                language_code=language_code,
            )

        if len(self.translation_language_codes) == 1:
            raise CannotDeleteOnlyPlaceCategoryTranslation(
                category_id=self.id,
                language_code=language_code,
            )

    def unregister_translation_language(self, language_code: LanguageEnum) -> None:
        self.translation_language_codes.remove(language_code)
