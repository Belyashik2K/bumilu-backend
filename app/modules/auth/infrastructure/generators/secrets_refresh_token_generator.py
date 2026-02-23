import secrets

from app.modules.auth.application.interfaces.generators import (
    IRefreshTokenGenerator,
)


class SecretsRefreshTokenGenerator(IRefreshTokenGenerator):
    def generate(self) -> str:
        return secrets.token_urlsafe(64)
