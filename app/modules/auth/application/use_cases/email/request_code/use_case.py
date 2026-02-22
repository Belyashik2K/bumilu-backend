from app.core.application.use_cases.base import IBaseUseCase
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
from app.modules.users.domain.value_objects import EmailVO


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
        ttl_seconds: int,
    ) -> None:
        self._code_generator = code_generator
        self._code_hasher = code_hasher
        self._challenge_store = challenge_store
        self._ttl_seconds = ttl_seconds

    async def __call__(
        self,
        input_data: RequestEmailCodeAtLoginInputDTO,
    ) -> RequestEmailCodeAtLoginOutputDTO:
        email = EmailVO(input_data.email)

        code = self._code_generator.generate()
        code_hash = self._code_hasher.hash(email=email, code=code)

        await self._challenge_store.save(
            email=email, code_hash=code_hash, ttl_seconds=self._ttl_seconds
        )

        print(
            f"Verification code for {email.value}: {code} (hash: {code_hash})"
        )  # In real application, send this code via email

        return RequestEmailCodeAtLoginOutputDTO()
