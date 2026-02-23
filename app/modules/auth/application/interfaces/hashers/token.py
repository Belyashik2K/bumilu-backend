from abc import ABC

from app.modules.auth.application.interfaces.hashers.base import IHasher


class ITokenHasher(IHasher, ABC): ...
