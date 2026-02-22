from app.core.application.use_cases.base import IBaseUseCase
from app.modules.auth.application.interfaces.repositories.auth_session import (
    IAuthSessionRepository,
)
from app.modules.auth.application.services.auth_session import AuthSessionService
from app.modules.auth.application.use_cases.refresh_session import (
    RefreshAuthSessionInputDTO,
    RefreshAuthSessionOutputDTO,
)
from app.modules.auth.application.use_cases.shared_dtos import (
    TokenInfoDTO,
    UserInfoDTO,
)
from app.modules.users.application.interfaces.repositories.user import IUserRepository


class RefreshAuthSessionUseCase(
    IBaseUseCase[
        RefreshAuthSessionInputDTO,
        RefreshAuthSessionOutputDTO,
    ]
):
    def __init__(
        self,
        auth_session_repository: IAuthSessionRepository,
        user_repository: IUserRepository,
        auth_session_service: AuthSessionService,
    ) -> None:
        self._auth_session_repository = auth_session_repository
        self._user_repository = user_repository
        self._auth_session_service = auth_session_service

    async def __call__(
        self,
        input_data: RefreshAuthSessionInputDTO,
    ) -> RefreshAuthSessionOutputDTO:
        token_hash = self._auth_session_service.get_token_hash(input_data.refresh_token)

        session = await self._auth_session_repository.get_by_refresh_token_hash(
            token_hash
        )

        if session is None or not session.is_active():
            raise ValueError("Invalid refresh token")

        if session.device_id != input_data.device_id:
            # TODO: complete VO to compare
            ...

        user = await self._user_repository.get_by_id(session.user_id)
        if user is None:
            raise ValueError("User not found")

        new_tokens = await self._auth_session_service.rotate(
            session=session,
            role=user.role,
        )

        return RefreshAuthSessionOutputDTO(
            access=TokenInfoDTO(
                token=new_tokens.access_token,
                expires_in=new_tokens.access_expires_in,
            ),
            refresh=TokenInfoDTO(
                token=new_tokens.refresh_token,
                expires_in=new_tokens.refresh_expires_in,
            ),
            user=UserInfoDTO(
                id=str(user.id),
                role=user.role,
            ),
        )
