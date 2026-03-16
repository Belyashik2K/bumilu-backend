from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.database import SQLAlchemyBaseRepository
from app.core.shared.domain.value_objects.id import (
    ChatIdVO,
    PrincipalIdVO,
)
from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.domain.models.chat import Chat
from app.modules.chat.domain.value_objects.location import LocationVO
from app.modules.chat.domain.value_objects.message_text import MessageTextVO
from app.modules.chat.infrastructure.database.models import ChatModel
from app.modules.chat.shared.enums import ChatStatusEnum


class SQLAlchemyChatRepository(
    IChatRepository, SQLAlchemyBaseRepository[Chat, ChatModel]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ChatModel)

    def _to_data(self, entity: Chat) -> ChatModel:
        return ChatModel(
            id=entity.id.value,
            user_id=entity.user_id.value if entity.user_id else None,
            language=entity.language,
            status=entity.status,
            last_location_latitude=entity.last_location.latitude
            if entity.last_location
            else None,
            last_location_longitude=entity.last_location.longitude
            if entity.last_location
            else None,
            last_message_preview=entity.last_message_preview.preview
            if entity.last_message_preview
            else None,
            last_activity_at=entity.last_activity_at,
            closed_at=entity.closed_at,
            close_reason=entity.close_reason,
        )

    def _to_entity(self, data: ChatModel) -> Chat:
        return Chat(
            id=ChatIdVO.from_uuid(data.id),
            user_id=PrincipalIdVO.from_uuid(data.user_id),
            language=data.language,
            status=data.status,
            last_location=LocationVO.from_coordinates(
                data.last_location_latitude, data.last_location_longitude
            ),
            last_message_preview=MessageTextVO(data.last_message_preview)
            if data.last_message_preview
            else None,
            last_activity_at=data.last_activity_at,
            closed_at=data.closed_at,
            close_reason=data.close_reason,
        )

    async def find_active_chat(self, user_id: PrincipalIdVO) -> Chat | None:
        stmt = select(ChatModel).where(
            ChatModel.user_id == user_id.value,
            ChatModel.status != ChatStatusEnum.CLOSED,
        )
        result = await self.session.execute(stmt)
        chat_model = result.scalar_one_or_none()
        if not chat_model:
            return None
        return self._to_entity(chat_model)

    async def get_active_chat_id(self, user_id: PrincipalIdVO) -> ChatIdVO | None:
        stmt = select(ChatModel.id).where(
            ChatModel.user_id == user_id.value,
            ChatModel.status != ChatStatusEnum.CLOSED,
        )
        result = await self.session.execute(stmt)
        chat_id = result.scalar_one_or_none()
        if not chat_id:
            return None
        return ChatIdVO.from_uuid(chat_id)

    async def get_pending_chats(self) -> list[Chat]:
        stmt = (
            select(ChatModel)
            .where(
                ChatModel.status == ChatStatusEnum.WAITING_FOR_AI,
            )
            .with_for_update(skip_locked=True)
        )
        result = await self.session.execute(stmt)
        chat_models = result.scalars().all()
        return [self._to_entity(chat_model) for chat_model in chat_models]

    async def get_inactive_open_chats(self, threshold: datetime) -> list[Chat]:
        stmt = (
            select(ChatModel)
            .where(
                ChatModel.status == ChatStatusEnum.ACTIVE,
                ChatModel.last_activity_at < threshold,
            )
            .with_for_update(skip_locked=True)
        )
        result = await self.session.execute(stmt)
        chat_models = result.scalars().all()
        return [self._to_entity(chat_model) for chat_model in chat_models]

    async def get_by_id_with_lock(self, chat_id: ChatIdVO) -> Chat | None:
        stmt = (
            select(ChatModel)
            .where(ChatModel.id == chat_id.value)
            .with_for_update(skip_locked=True)
        )
        result = await self.session.execute(stmt)
        chat = result.scalar_one_or_none()
        if not chat:
            return None
        return self._to_entity(chat)
