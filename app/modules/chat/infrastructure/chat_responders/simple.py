from random import random

from app.modules.chat.application.interfaces.chat_responder import (
    ChatResponderResult,
    IChatResponder,
)
from app.modules.chat.domain.models.chat import Chat
from app.modules.chat.domain.models.chat_message import ChatMessage


class SimpleChatResponder(IChatResponder):
    @staticmethod
    def _generate_confidence_score() -> float:
        return random()

    @staticmethod
    def _generate_reply_text(messages: list[ChatMessage]) -> str:
        if not messages:
            return "Hello! How can I assist you today?"
        last_message = messages[-1]
        return f"You said: '{last_message.text.value}'. How can I help you further?"

    async def generate_reply(
        self,
        chat: Chat,
        messages: list[ChatMessage],
    ) -> ChatResponderResult:
        confidence_score = self._generate_confidence_score()
        reply_text = self._generate_reply_text(messages)

        return ChatResponderResult(
            reply=reply_text,
            confidence_score=confidence_score,
        )
