from dataclasses import dataclass
from typing import ClassVar

from app.core.domain.value_objects.email.object import BaseEmailVO


@dataclass(frozen=True, slots=True)
class StaffEmailVO(BaseEmailVO):
    ALLOWED_DOMAINS: ClassVar[set[str]] = {
        "dev.bumilu.ru",
        "dev.isliteotw.ru",
        "dev.belyashik2k.de",
    }
