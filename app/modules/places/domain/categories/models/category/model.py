from dataclasses import (
    dataclass,
    field,
)
from typing import Self

from app.core.domain.value_objects.id import (
    PlaceCategoryIdVO,
)
from app.core.enums import LanguageEnum
from app.core.enums.language import REQUIRED_LANGUAGES
from app.modules.places.domain.categories.models.category.exceptions import (
    CannotPublishPlaceCategoryMissingTranslations,
    InvalidPlaceCategoryStatusTransition,
    PlaceCategoryIsNotEditable,
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
from app.modules.places.shared.enums.place_category_status import (
    PlaceCategoryStatusEnum,
)


@dataclass(slots=True, kw_only=True)
class PlaceCategory:
    id: PlaceCategoryIdVO
    slug: PlaceCategorySlugVO
    icon_key: PlaceCategoryIconKeyVO
    marker_color: PlaceCategoryMarkerColorVO
    status: PlaceCategoryStatusEnum = field(default=PlaceCategoryStatusEnum.DRAFT)
    translation_language_codes: set[LanguageEnum] = field(default_factory=set)

    def is_draft(self) -> bool:
        return self.status == PlaceCategoryStatusEnum.DRAFT

    def is_hidden(self) -> bool:
        return self.status == PlaceCategoryStatusEnum.HIDDEN

    def is_published(self) -> bool:
        return self.status == PlaceCategoryStatusEnum.PUBLISHED

    def is_editable(self) -> bool:
        return self.is_draft() or self.is_hidden()

    @classmethod
    def create(
        cls,
        slug: PlaceCategorySlugVO,
        icon_key: PlaceCategoryIconKeyVO,
        marker_color: PlaceCategoryMarkerColorVO,
    ) -> Self:
        return PlaceCategory(
            id=PlaceCategoryIdVO.new(),
            slug=slug,
            icon_key=icon_key,
            marker_color=marker_color,
        )

    def update(
        self,
        *,
        slug: PlaceCategorySlugVO | None = None,
        icon_key: PlaceCategoryIconKeyVO | None = None,
        marker_color: PlaceCategoryMarkerColorVO | None = None,
    ) -> None:
        if not self.is_editable():
            raise PlaceCategoryIsNotEditable(
                category_id=self.id,
            )

        if slug is not None and slug != self.slug:
            self.slug = slug
        if icon_key is not None and icon_key != self.icon_key:
            self.icon_key = icon_key
        if marker_color is not None and marker_color != self.marker_color:
            self.marker_color = marker_color

    def create_translation(
        self, data: NewPlaceCategoryTranslation
    ) -> PlaceCategoryTranslation:
        if not self.is_editable():
            raise PlaceCategoryIsNotEditable(
                category_id=self.id,
            )

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

    def publish(self) -> None:
        if self.is_published():
            return

        missing = REQUIRED_LANGUAGES - self.translation_language_codes
        if missing:
            raise CannotPublishPlaceCategoryMissingTranslations(
                category_id=self.id,
                missing_languages=missing,
            )
        self.status = PlaceCategoryStatusEnum.PUBLISHED

    def hide(self) -> None:
        if not self.is_published():
            raise InvalidPlaceCategoryStatusTransition(
                category_id=self.id,
                from_status=self.status,
                to_status=PlaceCategoryStatusEnum.HIDDEN,
            )
        self.status = PlaceCategoryStatusEnum.HIDDEN

    def ensure_translation_can_be_deleted(self, language_code: LanguageEnum) -> None:
        if not self.is_editable():
            raise PlaceCategoryIsNotEditable(
                category_id=self.id,
            )

        if language_code not in self.translation_language_codes:
            raise PlaceCategoryTranslationNotFound(
                category_id=self.id,
                language_code=language_code,
            )

    def remove_translation(
        self,
        language_code: LanguageEnum,
    ) -> None:
        self.ensure_translation_can_be_deleted(language_code=language_code)
        self.translation_language_codes.remove(language_code)
