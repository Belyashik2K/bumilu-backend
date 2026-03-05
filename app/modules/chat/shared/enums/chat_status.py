from enum import StrEnum


class ChatStatusEnum(StrEnum):
    ACTIVE = "active"
    WAITING_FOR_AI = "waiting_for_ai"
    ESCALATED = "escalated"
    CLOSED = "closed"
