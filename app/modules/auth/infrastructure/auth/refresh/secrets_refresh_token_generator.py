import secrets

from app.modules.auth.application.interfaces.refresh_token_generator import (
    IRefreshTokenGenerator,
)


class SecretsRefreshTokenGenerator(IRefreshTokenGenerator):
    def generate(self) -> str:
        return secrets.token_urlsafe(64)
