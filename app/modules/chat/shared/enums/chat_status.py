from enum import StrEnum


class ChatStatusEnum(StrEnum):
    ACTIVE = "active"
    WAITING_FOR_AI = "waiting_for_ai"
    ESCALATED_TO_ADMIN = "escalated_to_admin"
    CLOSED = "closed"
