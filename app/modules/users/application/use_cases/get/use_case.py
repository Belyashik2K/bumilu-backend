from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.domain.value_objects.id import UserIdVO
from app.modules.users.application.interfaces.repositories.user import IUserRepository
from app.modules.users.application.use_cases.get import (
    GetUserInputDTO,
    GetUserOutputDTO,
)
from app.modules.users.application.use_cases.get.exceptions import UserNotFound


class GetUserUseCase(
    IBaseUseCase[
        GetUserInputDTO,
        GetUserOutputDTO,
    ]
):
    def __init__(
        self,
        user_repository: IUserRepository,
    ) -> None:
        self._user_repository = user_repository

    async def execute(
        self,
        input_data: GetUserInputDTO,
    ) -> GetUserOutputDTO:
        user_id = UserIdVO.from_uuid(input_data.id)

        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound(user_id=user_id)

        return GetUserOutputDTO(
            id=str(user.id),
            email=str(user.email) if user.email else None,
            role=user.role,
        )
