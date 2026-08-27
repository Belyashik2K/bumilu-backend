import pytest
from app.core.domain.value_objects.email.exceptions import EmailDomainNotAllowed
from app.modules.users.domain.value_objects.user_email.object import UserEmailVO


class TestUserEmailVO:
    def test_accepts_regular_email(self) -> None:
        email = UserEmailVO.from_string("someone@gmail.com")

        assert email.value == "someone@gmail.com"

    def test_rejects_own_unowned_domain(self) -> None:
        with pytest.raises(EmailDomainNotAllowed):
            UserEmailVO.from_string("someone@bumi.lu")
