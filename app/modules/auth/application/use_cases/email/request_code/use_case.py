import logging

from app.core.application.use_cases.base import IBaseUseCase
from app.core.shared.utils import prepare_extras
from app.modules.auth.application.interfaces.email_sender import IEmailSender
from app.modules.auth.application.interfaces.generators import (
    IVerificationCodeGenerator,
)
from app.modules.auth.application.interfaces.hashers import IVerificationCodeHasher
from app.modules.auth.application.interfaces.stores.email_login import (
    IEmailLoginChallengeStore,
)
from app.modules.auth.application.use_cases.email.request_code import (
    RequestEmailCodeAtLoginInputDTO,
    RequestEmailCodeAtLoginOutputDTO,
)
from app.modules.auth.application.use_cases.email.request_code.exceptions import (
    VerificationCodeRequestedTooEarly,
)
from app.modules.users.domain.value_objects import EmailVO

logger = logging.getLogger(__name__)


class RequestEmailCodeAtLoginUseCase(
    IBaseUseCase[
        RequestEmailCodeAtLoginInputDTO,
        RequestEmailCodeAtLoginOutputDTO,
    ]
):
    def __init__(
        self,
        code_generator: IVerificationCodeGenerator,
        code_hasher: IVerificationCodeHasher,
        challenge_store: IEmailLoginChallengeStore,
        email_sender: IEmailSender,
        email_subject: str,
        email_body_template: str,
        resend_cooldown_seconds: int,
        ttl_seconds: int,
    ) -> None:
        self._code_generator = code_generator
        self._code_hasher = code_hasher
        self._challenge_store = challenge_store
        self._email_sender = email_sender
        self._email_subject = email_subject
        self._email_body_template = email_body_template
        self._resend_cooldown_seconds = resend_cooldown_seconds
        self._ttl_seconds = ttl_seconds

    async def execute(
        self,
        input_data: RequestEmailCodeAtLoginInputDTO,
    ) -> RequestEmailCodeAtLoginOutputDTO:
        email = EmailVO(input_data.email)

        code = self._code_generator.generate()
        code_hash = self._code_hasher.hash(email=email, code=code)

        retry_after = await self._challenge_store.save_with_rate_limit(
            email=email,
            code_hash=code_hash,
            ttl_seconds=self._ttl_seconds,
            min_interval_seconds=self._resend_cooldown_seconds,
        )
        if retry_after > 0:
            logger.warning(
                "email_login_code_request_rate_limited",
                extra=prepare_extras(
                    email=email.fingerprint, retry_after_seconds=retry_after
                ),
            )
            raise VerificationCodeRequestedTooEarly(retry_after_seconds=retry_after)

        await self._email_sender.send(
            to=email,
            subject=self._email_subject,
            body=self._email_body_template.format(
                code=code, ttl_min=self._ttl_seconds // 60
            ),
        )

        return RequestEmailCodeAtLoginOutputDTO()
