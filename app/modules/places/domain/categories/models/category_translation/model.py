from dataclasses import dataclass
from typing import Self

from app.core.domain.value_objects.id import (
    PlaceCategoryIdVO,
    PlaceCategoryTranslationIdVO,
)
from app.core.enums import LanguageEnum
from app.modules.places.domain.categories.value_objects.name.object import (
    PlaceCategoryNameVO,
)


# TODO: refactor as in places
@dataclass(frozen=True, slots=True, kw_only=True)
class NewPlaceCategoryTranslation:
    language_code: LanguageEnum
    name: PlaceCategoryNameVO


@dataclass(slots=True, kw_only=True)
class PlaceCategoryTranslation:
    id: PlaceCategoryTranslationIdVO
    category_id: PlaceCategoryIdVO
    language_code: LanguageEnum
    name: PlaceCategoryNameVO

    @classmethod
    def create(
        cls,
        category_id: PlaceCategoryIdVO,
        data: NewPlaceCategoryTranslation,
    ) -> Self:
        return cls(
            id=PlaceCategoryTranslationIdVO.new(),
            category_id=category_id,
            language_code=data.language_code,
            name=data.name,
        )

    def update(
        self,
        name: PlaceCategoryNameVO | None = None,
    ) -> None:
        if name is not None and name != self.name:
            self.name = name
