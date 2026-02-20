from enum import Enum


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
