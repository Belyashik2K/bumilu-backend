from dishka import (
    Provider,
    Scope,
    provide,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.chat.application.interfaces.repositories.chat import IChatRepository
from app.modules.chat.application.interfaces.repositories.chat_message import (
    IChatMessageRepository,
)
from app.modules.chat.application.queries.readers.chat import IChatReader
from app.modules.chat.application.queries.readers.chat_message import IChatMessageReader
from app.modules.chat.infrastructure.database.readers.chat import SQLAlchemyChatReader
from app.modules.chat.infrastructure.database.readers.chat_message import (
    SQLAlchemyChatMessageReader,
)
from app.modules.chat.infrastructure.database.repositories.chat import (
    SQLAlchemyChatRepository,
)
from app.modules.chat.infrastructure.database.repositories.chat_message import (
    SQLAlchemyChatMessageRepository,
)


class ChatPersistenceProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=IChatRepository)
    async def chat_repository(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyChatRepository:
        return SQLAlchemyChatRepository(session=session)

    @provide(scope=Scope.REQUEST, provides=IChatReader)
    async def chat_reader(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyChatReader:
        return SQLAlchemyChatReader(session=session)

    @provide(scope=Scope.REQUEST, provides=IChatMessageRepository)
    async def chat_message_repository(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyChatMessageRepository:
        return SQLAlchemyChatMessageRepository(session=session)

    @provide(scope=Scope.REQUEST, provides=IChatMessageReader)
    async def chat_message_reader(
        self,
        session: AsyncSession,
    ) -> SQLAlchemyChatMessageReader:
        return SQLAlchemyChatMessageReader(session=session)
