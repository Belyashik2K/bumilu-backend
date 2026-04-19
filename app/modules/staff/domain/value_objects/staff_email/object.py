from dataclasses import dataclass
from typing import ClassVar

from app.core.domain.value_objects.email.object import BaseEmailVO


@dataclass(frozen=True, slots=True)
class StaffMemberEmailVO(BaseEmailVO):
    ALLOWED_DOMAINS: ClassVar[set[str]] = {
        "bumilu.ru",
        "dev.bumilu.ru",
        "staff.bumilu.ru",
        "dev.isliteotw.ru",
        "dev.belyashik2k.de",
    }
