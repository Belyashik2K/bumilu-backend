import logging
import ssl
from collections.abc import Mapping
from email.message import EmailMessage
from email.utils import formataddr
from typing import (
    Any,
)

from aiosmtplib import (
    SMTP,
    SMTPException,
)

from app.core.shared.exceptions import BaseInfrastructureException
from app.core.shared.utils import prepare_extras
from app.modules.auth.application.interfaces.email_sender import IEmailSender
from app.modules.users.domain.value_objects import EmailVO

logger = logging.getLogger(__name__)


class EmailDeliveryFailed(BaseInfrastructureException):
    def __init__(self, context: Mapping[str, Any] | None = None) -> None:
        super().__init__(
            message="Failed to deliver email",
            context=context,
        )


class SMTPLibEmailSender(IEmailSender):
    def __init__(
        self,
        host: str,
        port: int,
        login: str,
        password: str,
        from_author: str,
        from_email: str,
        timeout: int = 30,
    ) -> None:
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.from_author = from_author
        self.from_email = from_email
        self.timeout = timeout

        self._tls_context = ssl.create_default_context()

    def _get_context(
        self,
        to: EmailVO,
        *,
        error_type: str | None = None,
    ) -> dict:
        return prepare_extras(
            provider="smtp",
            to=to.fingerprint,
            host=self.host,
            port=self.port,
            error_type=error_type,
        )

    async def send(self, to: EmailVO, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = formataddr((self.from_author, self.from_email))
        message["To"] = str(to)
        message["Subject"] = subject
        message.set_content(body)

        smtp = SMTP(
            hostname=self.host,
            port=self.port,
            use_tls=True,
            tls_context=self._tls_context,
            timeout=self.timeout,
        )

        try:
            await smtp.connect()
            await smtp.login(self.login, self.password)
            await smtp.send_message(message)
            logger.debug(
                "email_login_smtp_sent",
                extra=self._get_context(to),
            )
        except SMTPException as e:
            raise EmailDeliveryFailed(context=self._get_context(to=to)) from e
        finally:
            try:
                await smtp.quit()
            except Exception as e:
                logger.debug(
                    "email_login_smtp_quit_failed",
                    extra=self._get_context(to, error_type=type(e).__name__),
                )
