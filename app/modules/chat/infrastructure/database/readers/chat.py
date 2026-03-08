from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat.application.queries.readers.chat import IChatReader
from app.modules.chat.application.queries.user.get_chat import UserChatView
from app.modules.chat.infrastructure.database.models import ChatModel
from app.modules.chat.shared.enums import ChatStatusEnum


class SQLAlchemyChatReader(IChatReader):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_active_chat_by_user_id(self, user_id: UUID) -> UserChatView | None:
        stmt = select(ChatModel.id, ChatModel.status, ChatModel.last_activity_at).where(
            ChatModel.user_id == user_id, ChatModel.status != ChatStatusEnum.CLOSED
        )
        result = await self._session.execute(stmt)
        row = result.first()
        if not row:
            return None
        return UserChatView(
            id=row.id, status=row.status, last_activity_at=row.last_activity_at
        )
