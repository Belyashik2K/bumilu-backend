import logging
import ssl
from email.message import EmailMessage
from email.utils import formataddr

from aiosmtplib import (
    SMTP,
    SMTPException,
)

from app.core.shared.utils import prepare_extras
from app.modules.auth.application.interfaces.email_sender import IEmailSender
from app.modules.users.domain.value_objects import EmailVO

logger = logging.getLogger(__name__)


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

    def _get_extras(
        self,
        to: EmailVO,
        *,
        error: Exception | None = None,
    ) -> dict:
        return prepare_extras(
            to=to.fingerprint, host=self.host, port=self.port, error=error
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
                extra=self._get_extras(to),
            )
        except SMTPException:
            logger.exception(
                "email_login_smtp_sending_failed", extra=self._get_extras(to)
            )
            raise
        finally:
            try:
                await smtp.quit()
            except Exception as e:
                logger.warning(
                    "email_login_smtp_quit_failed", extra=self._get_extras(to, error=e)
                )
                pass
