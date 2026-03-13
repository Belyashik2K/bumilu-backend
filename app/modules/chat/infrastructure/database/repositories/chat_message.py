from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.infrastructure.database import SQLAlchemyBaseRepository
from app.core.shared.domain.value_objects.id import (
    ChatIdVO,
    ChatMessageIdVO,
    PrincipalIdVO,
)
from app.modules.chat.application.interfaces.repositories.chat_message import (
    IChatMessageRepository,
)
from app.modules.chat.domain.models.chat_message import ChatMessage
from app.modules.chat.domain.value_objects.location import LocationVO
from app.modules.chat.domain.value_objects.message_text import MessageTextVO
from app.modules.chat.infrastructure.database.models import ChatMessageModel


class SQLAlchemyChatMessageRepository(
    IChatMessageRepository, SQLAlchemyBaseRepository[ChatMessage, ChatMessageModel]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ChatMessageModel)

    def _to_data(self, entity: ChatMessage) -> ChatMessageModel:
        return ChatMessageModel(
            id=entity.id.value,
            chat_id=entity.chat_id.value,
            author_id=entity.author_id.value if entity.author_id else None,
            author_type=entity.author_type,
            text=entity.text.value,
            location_latitude=entity.location.latitude if entity.location else None,
            location_longitude=entity.location.longitude if entity.location else None,
        )

    def _to_entity(self, data: ChatMessageModel) -> ChatMessage:
        return ChatMessage(
            id=ChatMessageIdVO.from_uuid(data.id),
            chat_id=ChatIdVO.from_uuid(data.chat_id),
            author_id=PrincipalIdVO.from_uuid(data.author_id)
            if data.author_id
            else None,
            author_type=data.author_type,
            text=MessageTextVO(data.text),
            location=LocationVO.from_coordinates(
                data.location_latitude, data.location_longitude
            ),
        )

    async def get_chat_messages(self, chat_id: ChatIdVO) -> list[ChatMessage]:
        stmt = (
            select(ChatMessageModel)
            .where(ChatMessageModel.chat_id == chat_id.value)
            .order_by(ChatMessageModel.created_at)
        )
        result = await self.session.execute(stmt)
        return [self._to_entity(message) for message in result.scalars().all()]

    async def batch_get_chat_messages(
        self, chat_ids: Iterable[ChatIdVO]
    ) -> dict[ChatIdVO, list[ChatMessage]]:
        stmt = (
            select(ChatMessageModel)
            .where(
                ChatMessageModel.chat_id.in_([chat_id.value for chat_id in chat_ids])
            )
            .order_by(ChatMessageModel.created_at)
        )
        result = await self.session.execute(stmt)
        messages_by_chat_id: dict[ChatIdVO, list[ChatMessage]] = {}
        for message_data in result.scalars().all():
            message = self._to_entity(message_data)
            messages_by_chat_id.setdefault(message.chat_id, []).append(message)
        return messages_by_chat_id
