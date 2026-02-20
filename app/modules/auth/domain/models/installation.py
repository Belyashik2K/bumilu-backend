from dataclasses import dataclass

from app.core.shared.domain.value_objects.id import (
    InstallationIdVO,
    UserIdVO,
)


@dataclass(slots=True, kw_only=True)
class Installation:
    id: InstallationIdVO
    user_id: UserIdVO
