from secrets import choice
from string import digits

from app.modules.auth.application.interfaces.generators import (
    IVerificationCodeGenerator,
)


class SecretsVerificationCodeGenerator(IVerificationCodeGenerator):
    def __init__(self, code_length: int) -> None:
        self._code_length = code_length

    def generate(self) -> str:
        return "".join(choice(digits) for _ in range(self._code_length))
