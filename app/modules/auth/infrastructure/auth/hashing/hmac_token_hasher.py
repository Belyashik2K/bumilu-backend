import base64
import hashlib
import hmac

from app.modules.auth.application.interfaces.hashers import ITokenHasher


class HMACTokenHasher(ITokenHasher):
    def __init__(self, secret: str) -> None:
        self._secret = secret.encode("utf-8")

    def _digest(self, token: str) -> str:
        mac = hmac.new(
            self._secret,
            token.encode("utf-8"),
            hashlib.sha256,
        ).digest()

        return base64.urlsafe_b64encode(mac).decode("ascii").rstrip("=")

    def hash(self, token: str) -> str:
        return self._digest(token)

    def verify(self, token: str, hashed_token: str) -> bool:
        expected = self._digest(token)
        return hmac.compare_digest(expected, hashed_token)
