from enum import StrEnum


class ChatCloseReasonEnum(StrEnum):
    BY_ADMIN = "by_admin"
    INACTIVITY = "inactivity"
