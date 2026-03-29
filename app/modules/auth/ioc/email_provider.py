from dishka import (
    Provider,
    Scope,
    provide,
)

from app.core.infrastructure.config import AppConfig
from app.modules.auth.application.interfaces.email_sender import IEmailSender
from app.modules.auth.infrastructure.smtplib_email_sender import SMTPLibEmailSender


class AuthEmailProvider(Provider):
    @provide(scope=Scope.APP, provides=IEmailSender)
    async def email_sender(
        self,
        config: AppConfig,
    ) -> IEmailSender:
        return SMTPLibEmailSender(
            host=config.auth.email.smtp.host,
            port=config.auth.email.smtp.port,
            login=config.auth.email.smtp.username,
            password=config.auth.email.smtp.password,
            from_author=config.auth.email.smtp.from_name,
            from_email=config.auth.email.smtp.from_email,
            timeout=config.auth.email.smtp.timeout,
        )
