from dataclasses import dataclass
from typing import ClassVar

from app.core.domain.value_objects.email.object import BaseEmailVO


@dataclass(frozen=True, slots=True)
class UserEmailVO(BaseEmailVO):
    BLOCKED_DOMAINS: ClassVar[set[str]] = {
        "bumi.lu"
    }  # вот когда сами купим, тогда и пропустим
