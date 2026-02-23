import hashlib
import hmac

from app.modules.auth.application.interfaces.hashers import IVerificationCodeHasher
from app.modules.users.domain.value_objects import EmailVO


class HMACVerificationCodeHasher(IVerificationCodeHasher):
    def __init__(self, secret: str) -> None:
        self._secret = secret.encode("utf-8")

    @staticmethod
    def _build_message(email: EmailVO, code: str) -> bytes:
        message = f"{email!s}:{code}"
        return message.encode("utf-8")

    def hash(self, *, email: EmailVO, code: str) -> str:
        msg = self._build_message(email=email, code=code)
        return hmac.new(self._secret, msg, hashlib.sha256).hexdigest()

    def verify(self, *, email: EmailVO, code: str, code_hash: str) -> bool:
        expected_hash = self.hash(email=email, code=code)
        return hmac.compare_digest(expected_hash, code_hash)
