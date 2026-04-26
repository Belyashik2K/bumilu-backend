import json
from typing import (
    Any,
)

from openai import AsyncOpenAI

from app.modules.chat.application.interfaces.chat_responder import (
    ChatResponderResult,
    IChatResponder,
)
from app.modules.chat.application.interfaces.location_context_provider import (
    LocationContext,
)
from app.modules.chat.domain.models.chat import Chat
from app.modules.chat.domain.models.chat_message import ChatMessage
from app.modules.chat.shared.enums import AuthorTypeEnum


class OpenAIChatResponder(IChatResponder):
    def __init__(
        self,
        api_key: str,
        api_base_url: str,
        model: str,
        system_prompt: str,
    ) -> None:
        self._model = model
        self._system_prompt = system_prompt
        self._client = AsyncOpenAI(
            base_url=api_base_url,
            api_key=api_key,
        )

    async def generate_reply(
        self,
        chat: Chat,
        messages: list[ChatMessage],
        location_context: LocationContext | None = None,
    ) -> ChatResponderResult:
        llm_messages = self._build_messages(
            chat=chat, messages=messages, location_context=location_context
        )
        raw_content = await self._generate_completion(messages=llm_messages)
        return self._parse_response(raw_content)

    def _build_messages(
        self,
        chat: Chat,
        messages: list[ChatMessage],
        location_context: LocationContext | None = None,
    ) -> list[dict[str, str]]:
        system_prompt = self._build_system_prompt(
            chat=chat, location_context=location_context
        )

        llm_messages: list[dict[str, str]] = [
            {"role": "system", "content": system_prompt},
        ]

        for message in messages:
            llm_messages.append(
                {
                    "role": self._map_role(message),
                    "content": message.text.value,
                }
            )

        return llm_messages

    def _build_system_prompt(
        self, chat: Chat, location_context: LocationContext
    ) -> str:
        prompt_parts: list[str] = [
            self._system_prompt.strip(),
            f"User language: {chat.language.value}",
        ]

        if chat.last_location is not None:
            prompt_parts.append(
                "Current user location has changed or may have changed. "
                "Always treat the last known user location below as the source of truth. "
                "Do not use locations from previous messages unless the user explicitly asks about them.\n"
                f"Current location: lat={chat.last_location.latitude}, "
                f"lon={chat.last_location.longitude}"
            )

        if location_context is not None:
            prompt_parts.append(
                "Nearby places are based on the current user location. "
                "Use only these places when recommending nearby places. "
                "Do not invent places. "
                "If none of these places fit the user's request, ask a clarification question.\n"
                "Nearby places:\n"
                + json.dumps(
                    location_context.nearby_places,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    default=str,
                )
            )

        return "\n\n".join(prompt_parts)

    @staticmethod
    def _map_role(message: ChatMessage) -> str:
        if message.author_type == AuthorTypeEnum.AI:
            return "assistant"
        return "user"

    async def _generate_completion(self, messages: list[dict[str, str]]) -> str:
        completion = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,  # type: ignore
            temperature=0.2,
        )

        content = completion.choices[0].message.content
        if not content:
            return ""

        return content.strip()

    def _parse_response(self, raw_content: str) -> ChatResponderResult:
        try:
            payload = self._extract_json(raw_content)
            return self._build_result(payload)
        except Exception:
            return ChatResponderResult(
                reply=raw_content.strip()
                or "Content is empty or not in expected format.",
                confidence_score=0.2,
            )

    def _extract_json(self, raw_content: str) -> dict[str, Any]:
        text = raw_content.strip()

        try:
            data = json.loads(text)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

        fenced = self._extract_from_code_fence(text)
        if fenced is not None:
            data = json.loads(fenced)
            if isinstance(data, dict):
                return data

        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and start < end:
            candidate = text[start : end + 1]
            data = json.loads(candidate)
            if isinstance(data, dict):
                return data

        raise ValueError("JSON object not found in model response")

    @staticmethod
    def _extract_from_code_fence(text: str) -> str | None:
        if "```" not in text:
            return None

        parts = text.split("```")
        for part in parts:
            candidate = part.strip()
            if not candidate:
                continue

            if candidate.startswith("json"):
                candidate = candidate[4:].strip()

            if candidate.startswith("{") and candidate.endswith("}"):
                return candidate

        return None

    def _build_result(self, payload: dict[str, Any]) -> ChatResponderResult:
        reply = str(payload.get("reply", "")).strip()
        confidence_score = self._normalize_confidence(
            payload.get("confidence_score", 0.0)
        )

        if not reply:
            reply = "Content is empty or not in expected format."
            confidence_score = min(confidence_score, 0.2)

        return ChatResponderResult(
            reply=reply,
            confidence_score=confidence_score,
        )

    @staticmethod
    def _normalize_confidence(value: Any) -> float:
        try:
            confidence = float(value)
        except (TypeError, ValueError):
            return 0.0

        return max(0.0, min(1.0, confidence))
