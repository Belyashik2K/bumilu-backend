from uuid import UUID

from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.modules.chat.application.queries.admin.get_chat.view import AdminChatView
from app.modules.chat.application.queries.admin.get_chat_list.view import (
    AdminChatListPage,
    AdminChatPreviewView,
)
from app.modules.chat.application.queries.common_views import (
    LocationView,
    UserView,
)
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

    async def get_admin_chat_by_id(self, chat_id: UUID) -> AdminChatView | None:
        stmt = (
            select(ChatModel)
            .options(joinedload(ChatModel.user))
            .where(ChatModel.id == chat_id)
        )

        result = await self._session.execute(stmt)
        chat = result.scalar_one_or_none()
        if not chat:
            return None
        return AdminChatView(
            id=chat.id,
            user=UserView(
                id=chat.user.id,
                email=chat.user.email,
                role=chat.user.role,
            ),
            status=chat.status,
            language=chat.language,
            created_at=chat.created_at,
            last_activity_at=chat.last_activity_at,
            last_location=LocationView(
                latitude=chat.last_location_latitude,
                longitude=chat.last_location_longitude,
            )
            if chat.last_location_latitude and chat.last_location_longitude
            else None,
            closed_at=chat.closed_at,
            close_reason=chat.close_reason,
        )

    async def list_admin_chats(
        self,
        limit: int,
        offset: int,
        status: ChatStatusEnum | None = None,
    ) -> AdminChatListPage:
        count_stmt = select(func.count()).select_from(ChatModel)
        items_stmt = select(ChatModel).options(joinedload(ChatModel.user))

        if status is not None:
            count_stmt = count_stmt.where(ChatModel.status == status)
            items_stmt = items_stmt.where(ChatModel.status == status)

        total_subquery = count_stmt.scalar_subquery()

        stmt = (
            items_stmt.add_columns(total_subquery.label("total_count"))
            .order_by(ChatModel.created_at.asc())
            .limit(limit)
            .offset(offset)
        )

        result = await self._session.execute(stmt)
        rows = result.all()

        if not rows:
            total = await self._session.scalar(count_stmt)
            return AdminChatListPage(
                items=[],
                total=total or 0,
            )

        chats: list[ChatModel] = [row.ChatModel for row in rows]
        total = rows[0].total_count

        converted_chats = [
            AdminChatPreviewView(
                id=chat.id,
                user=UserView(
                    id=chat.user.id,
                    email=chat.user.email,
                    role=chat.user.role,
                ),
                language=chat.language,
                status=chat.status,
                last_activity_at=chat.last_activity_at,
                last_message_preview=chat.last_message_preview,
                last_location=LocationView(
                    latitude=chat.last_location_latitude,
                    longitude=chat.last_location_longitude,
                )
                if chat.last_location_latitude and chat.last_location_longitude
                else None,
            )
            for chat in chats
        ]

        return AdminChatListPage(
            items=converted_chats,
            total=total,
        )
