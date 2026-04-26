from dishka import (
    Provider,
    Scope,
    provide,
)

from app.core.infrastructure.config import AppConfig
from app.modules.chat.application.interfaces.chat_reply_dispatcher import (
    IChatReplyDispatcher,
)
from app.modules.chat.application.interfaces.chat_responder import IChatResponder
from app.modules.chat.application.interfaces.location_context_provider import (
    ILocationContextProvider,
)
from app.modules.chat.infrastructure.chat_responders.openai import OpenAIChatResponder
from app.modules.chat.infrastructure.location_context_provider import (
    LocationContextProvider,
)
from app.modules.chat.infrastructure.queue.dispatchers.taskiq_chat_reply_dispatcher import (
    TaskiqChatReplyDispatcher,
)
from app.modules.places.application.interfaces.readers.place import IPlaceReader


class ChatInfrastructureProvider(Provider):
    @provide(scope=Scope.APP, provides=IChatResponder)
    def openai_chat_responder(
        self,
        config: AppConfig,
    ) -> OpenAIChatResponder:
        return OpenAIChatResponder(
            api_key=config.chat.ai_assistant.openai.api_key,
            api_base_url=config.chat.ai_assistant.openai.api_base_url,
            model=config.chat.ai_assistant.openai.model,
            system_prompt=config.chat.ai_assistant.system_prompt,
        )

    @provide(scope=Scope.APP, provides=IChatReplyDispatcher)
    async def chat_reply_dispatcher(
        self,
    ) -> TaskiqChatReplyDispatcher:
        return TaskiqChatReplyDispatcher()

    @provide(scope=Scope.REQUEST, provides=ILocationContextProvider)
    async def location_context_provider(
        self,
        place_reader: IPlaceReader,
    ) -> LocationContextProvider:
        return LocationContextProvider(place_reader=place_reader)
