from uuid import UUID

from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat.application.queries.common_views import (
    ChatMessageAuthorView,
    ChatMessagesPage,
    ChatMessageView,
    LocationView,
)
from app.modules.chat.application.queries.readers.chat_message import IChatMessageReader
from app.modules.chat.infrastructure.database.models import ChatMessageModel


class SQLAlchemyChatMessageReader(IChatMessageReader):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    @staticmethod
    def to_view(data: ChatMessageModel) -> ChatMessageView:
        author = ChatMessageAuthorView(
            id=data.author_id,
            type=data.author_type,
        )

        location = (
            LocationView(
                latitude=data.location_latitude,
                longitude=data.location_longitude,
            )
            if data.location_latitude and data.location_longitude
            else None
        )

        return ChatMessageView(
            id=data.id,
            text=data.text,
            created_at=data.created_at,
            author=author,
            location=location,
        )

    async def list_messages_by_chat_id(
        self,
        chat_id: UUID,
        limit: int,
        offset: int,
    ) -> ChatMessagesPage:
        total_subquery = (
            select(func.count())
            .where(ChatMessageModel.chat_id == chat_id)
            .scalar_subquery()
        )

        stmt = (
            select(ChatMessageModel, total_subquery.label("total_count"))
            .where(ChatMessageModel.chat_id == chat_id)
            .order_by(ChatMessageModel.created_at.asc())
            .limit(limit)
            .offset(offset)
        )

        result = await self._session.execute(stmt)
        rows = result.all()

        if not rows:
            total = await self._session.scalar(
                select(func.count()).where(ChatMessageModel.chat_id == chat_id)
            )

            return ChatMessagesPage(
                items=[],
                total=total or 0,
            )

        messages = [self.to_view(row.ChatMessageModel) for row in rows]
        total = rows[0].total_count

        return ChatMessagesPage(
            items=messages,
            total=total,
        )
