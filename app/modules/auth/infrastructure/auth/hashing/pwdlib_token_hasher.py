import pwdlib

from app.modules.auth.application.interfaces.token_hasher import ITokenHasher


class PWDLibTokenHasher(ITokenHasher):
    def __init__(self) -> None:
        self._ctx = pwdlib.PasswordHash.recommended()

    def hash(self, token: str) -> str:
        return self._ctx.hash(token)

    def verify(self, token: str, hashed_token: str) -> bool:
        return self._ctx.verify(token, hashed_token)
