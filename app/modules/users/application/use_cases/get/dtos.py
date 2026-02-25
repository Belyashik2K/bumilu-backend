from dataclasses import dataclass
from uuid import UUID

from app.modules.users.application.use_cases.shared_dtos import UserInfoDTO


@dataclass(frozen=True, slots=True)
class GetUserInputDTO:
    id: UUID


class GetUserOutputDTO(UserInfoDTO): ...
