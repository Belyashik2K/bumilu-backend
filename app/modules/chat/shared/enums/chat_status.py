from enum import StrEnum


class ChatStatusEnum(StrEnum):
    ACTIVE = "active"
    NEEDS_HUMAN = "needs_human"
    CLOSED = "closed"
