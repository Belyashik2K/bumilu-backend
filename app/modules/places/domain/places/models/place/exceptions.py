from app.core.domain.value_objects.id import PlaceIdVO
from app.core.exceptions.domain.base import DomainInvariantViolationException


class PlaceIsNotEditable(DomainInvariantViolationException):
    def __init__(self, place_id: PlaceIdVO) -> None:
        super().__init__(
            message=f"Place with id {place_id} is not editable because it is published"
        )
