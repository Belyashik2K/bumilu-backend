import contextlib
import ssl
from email.message import EmailMessage
from email.utils import formataddr

from aiosmtplib import (
    SMTP,
    SMTPException,
)

from app.modules.auth.application.interfaces.email_sender import IEmailSender
from app.modules.users.domain.value_objects import EmailVO


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

        with contextlib.suppress(SMTPException):  # TODO: handle exceptions properly
            await smtp.connect()
            await smtp.login(self.login, self.password)
            await smtp.send_message(message)
            await smtp.quit()
