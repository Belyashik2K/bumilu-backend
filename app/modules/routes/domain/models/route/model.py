from collections.abc import Sequence
from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Self,
)

from app.core.domain.value_objects.id import (
    PlaceIdVO,
    RouteIdVO,
)
from app.core.enums import LanguageEnum
from app.modules.routes.domain.models.route_point.model import RoutePoint
from app.modules.routes.domain.models.route_translation.model import RouteTranslation
from app.modules.routes.domain.value_objects.description.object import (
    RouteDescriptionVO,
)
from app.modules.routes.domain.value_objects.point_index.object import RoutePointIndexVO
from app.modules.routes.domain.value_objects.short_description.object import (
    RouteShortDescriptionVO,
)
from app.modules.routes.domain.value_objects.title.object import RouteTitleVO
from app.modules.routes.shared.enums.route_status import RouteStatusEnum


@dataclass(slots=True, kw_only=True)
class Route:
    id: RouteIdVO
    status: RouteStatusEnum

    _points: list[RoutePoint] | None = field(default_factory=list)
    _translations: list[RouteTranslation] | None = field(default_factory=list)

    def is_draft(self) -> bool:
        return self.status == RouteStatusEnum.DRAFT

    def is_hidden(self) -> bool:
        return self.status == RouteStatusEnum.HIDDEN

    def is_published(self) -> bool:
        return self.status == RouteStatusEnum.PUBLISHED

    def is_editable(self) -> bool:
        return self.is_draft() or self.is_hidden()

    @classmethod
    def create(cls) -> Self:
        return cls(
            id=RouteIdVO.new(),
            status=RouteStatusEnum.DRAFT,
            _points=[],
            _translations=[],
        )

    @property
    def points(self) -> tuple[RoutePoint, ...]:
        if self._points is None:
            raise ValueError("Route points not loaded")
        return tuple(self._points)

    @property
    def translations(self) -> tuple[RouteTranslation, ...]:
        if self._translations is None:
            raise ValueError("Route translations not loaded")
        return tuple(self._translations)

    def replace_points(self, place_ids: Sequence[PlaceIdVO]) -> None:
        if not self.is_editable():
            raise ValueError("Only routes in DRAFT or HIDDEN status can be edited")

        if self._points is None:
            raise ValueError("Route points not loaded")

        self._points = [
            RoutePoint.create(
                route_id=self.id,
                place_id=place_id,
                index=RoutePointIndexVO(index),
            )
            for index, place_id in enumerate(place_ids)
        ]

    def find_translation(self, language_code: LanguageEnum) -> RouteTranslation | None:
        if self._translations is None:
            raise ValueError("Route translations not loaded")

        for translation in self._translations:
            if translation.language_code == language_code:
                return translation
        return None

    def has_translation(self, language_code: LanguageEnum) -> bool:
        return self.find_translation(language_code) is not None

    def add_translation(
        self,
        *,
        language_code: LanguageEnum,
        title: RouteTitleVO,
        short_description: RouteShortDescriptionVO,
        description: RouteDescriptionVO,
    ) -> RouteTranslation:
        if not self.is_editable():
            raise ValueError("Only routes in DRAFT or HIDDEN status can be edited")

        if self._translations is None:
            raise ValueError("Route translations not loaded")

        if self.has_translation(language_code):
            raise ValueError(
                f"Translation for language '{language_code}' already exists"
            )

        translation = RouteTranslation.create(
            route_id=self.id,
            language_code=language_code,
            title=title,
            short_description=short_description,
            description=description,
        )

        self._translations.append(translation)
        return translation

    def update_translation(
        self,
        *,
        language_code: LanguageEnum,
        title: RouteTitleVO | None = None,
        short_description: RouteShortDescriptionVO | None = None,
        description: RouteDescriptionVO | None = None,
    ) -> None:
        if not self.is_editable():
            raise ValueError("Only routes in DRAFT or HIDDEN status can be edited")

        if self._translations is None:
            raise ValueError("Route translations not loaded")

        translation = self.find_translation(language_code)
        if translation is None:
            raise ValueError(f"Translation for language '{language_code}' not found")

        translation.update(
            title=title,
            short_description=short_description,
            description=description,
        )

    def remove_translation(self, language_code: LanguageEnum) -> None:
        if not self.is_editable():
            raise ValueError("Only routes in DRAFT or HIDDEN status can be edited")

        if self._translations is None:
            raise ValueError("Route translations not loaded")

        initial_len = len(self._translations)

        self._translations = [
            translation
            for translation in self._translations
            if translation.language_code != language_code
        ]

        if len(self._translations) == initial_len:
            raise ValueError(f"Translation for language '{language_code}' not found")
