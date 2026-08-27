import pytest
from app.core.domain.value_objects.email.exceptions import EmailDomainNotAllowed
from app.modules.staff.domain.value_objects.staff_email.object import (
    StaffMemberEmailVO,
)


class TestStaffMemberEmailVO:
    @pytest.mark.parametrize(
        "raw",
        [
            "someone@bumilu.ru",
            "someone@dev.bumilu.ru",
            "someone@staff.bumilu.ru",
        ],
    )
    def test_accepts_whitelisted_domain(self, raw: str) -> None:
        email = StaffMemberEmailVO.from_string(raw)

        assert email.value == raw

    def test_rejects_domain_outside_whitelist(self) -> None:
        with pytest.raises(EmailDomainNotAllowed):
            StaffMemberEmailVO.from_string("someone@gmail.com")
