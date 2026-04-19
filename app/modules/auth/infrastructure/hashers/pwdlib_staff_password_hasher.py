from pwdlib import PasswordHash

from app.modules.auth.application.interfaces.hashers import IStaffPasswordHasher


class PWDLibStaffPasswordHasher(IStaffPasswordHasher):
    def __init__(self) -> None:
        self._password_hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self._password_hash.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        return self._password_hash.verify(password, password_hash)
