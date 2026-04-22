from app.core.domain.value_objects.id import (
    PlaceIdVO,
    RouteIdVO,
    RoutePointIdVO,
)
from app.core.enums import LanguageEnum
from app.core.exceptions.domain.base import (
    DomainInvariantViolationException,
    DomainNotFoundException,
)
from app.modules.routes.shared.enums.route_status import RouteStatusEnum


class RouteIsNotEditable(DomainInvariantViolationException):
    def __init__(self, route_id: RouteIdVO) -> None:
        super().__init__(
            message=f"Route with id {route_id} is not editable because it is published"
        )


class RouteTranslationAlreadyExists(DomainInvariantViolationException):
    def __init__(self, route_id: RouteIdVO, language_code: LanguageEnum) -> None:
        super().__init__(
            message=f"Translation for route with id {route_id} and language code {language_code} already exists"
        )


class RouteTranslationNotFound(DomainNotFoundException):
    def __init__(self, route_id: RouteIdVO, language_code: LanguageEnum) -> None:
        super().__init__(
            message=f"Translation for route with id {route_id} and language code {language_code} not found"
        )


class RoutePointNotFound(DomainNotFoundException):
    def __init__(self, route_id: RouteIdVO, point_id: RoutePointIdVO) -> None:
        super().__init__(
            message=f"Point with id {point_id} not found in route with id {route_id}"
        )


class CannotPublishPlaceMissingTranslations(DomainInvariantViolationException):
    def __init__(
        self,
        route_id: RouteIdVO,
        missing_languages: list[LanguageEnum],
    ) -> None:
        super().__init__(
            message=f"Cannot publish place with id {route_id} because it has missing translations for languages: "
            f"{', '.join(missing_languages)}",
        )


class CannotPublishRouteMissingPoints(DomainInvariantViolationException):
    def __init__(self, route_id: RouteIdVO) -> None:
        super().__init__(
            message=f"Cannot publish route with id {route_id} because it has less than 2 points",
        )


class CannotPublishRouteWithUnpublishedPlaces(DomainInvariantViolationException):
    def __init__(
        self,
        route_id: RouteIdVO,
        unpublished_place_ids: list[PlaceIdVO],
    ) -> None:
        super().__init__(
            message=f"Cannot publish route with id {route_id} because it has unpublished places with ids: "
            f"{', '.join(str(place_id) for place_id in unpublished_place_ids)}",
        )


class InvalidRouteStatusTransition(DomainInvariantViolationException):
    def __init__(
        self,
        route_id: RouteIdVO,
        from_status: RouteStatusEnum,
        to_status: RouteStatusEnum,
    ) -> None:
        super().__init__(
            message=f"Cannot change status of route with id {route_id} from {from_status} to {to_status}",
        )
