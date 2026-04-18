from dataclasses import dataclass

from app.core.domain.value_objects.id import (
    RouteIdVO,
    RouteTranslationIdVO,
)
from app.core.enums import LanguageEnum
from app.modules.routes.domain.value_objects.description.object import (
    RouteDescriptionVO,
)
from app.modules.routes.domain.value_objects.short_description.object import (
    RouteShortDescriptionVO,
)
from app.modules.routes.domain.value_objects.title.object import RouteTitleVO


@dataclass(slots=True, kw_only=True)
class RouteTranslation:
    id: RouteTranslationIdVO
    route_id: RouteIdVO
    language_code: LanguageEnum
    title: RouteTitleVO
    short_description: RouteShortDescriptionVO
    description: RouteDescriptionVO

    @classmethod
    def create(
        cls,
        route_id: RouteIdVO,
        language_code: LanguageEnum,
        title: RouteTitleVO,
        short_description: RouteShortDescriptionVO,
        description: RouteDescriptionVO,
    ) -> "RouteTranslation":
        return cls(
            id=RouteTranslationIdVO.new(),
            route_id=route_id,
            language_code=language_code,
            title=title,
            short_description=short_description,
            description=description,
        )

    def update(
        self,
        title: RouteTitleVO | None = None,
        short_description: RouteShortDescriptionVO | None = None,
        description: RouteDescriptionVO | None = None,
    ) -> None:
        if title is not None and title != self.title:
            self.title = title
        if (
            short_description is not None
            and short_description != self.short_description
        ):
            self.short_description = short_description
        if description is not None and description != self.description:
            self.description = description
