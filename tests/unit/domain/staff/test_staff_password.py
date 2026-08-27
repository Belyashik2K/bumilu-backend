import pytest
from app.core.domain.value_objects.string.exceptions import InvalidString
from app.modules.staff.domain.value_objects.staff_password.exception import (
    InvalidStaffMemberPassword,
)
from app.modules.staff.domain.value_objects.staff_password.object import (
    StaffMemberPasswordVO,
)


class TestStaffMemberPasswordVO:
    def test_accepts_password_meeting_all_requirements(self) -> None:
        password = StaffMemberPasswordVO("Str0ng!Pass")

        assert password.value == "Str0ng!Pass"

    def test_raises_when_missing_uppercase(self) -> None:
        with pytest.raises(InvalidStaffMemberPassword):
            StaffMemberPasswordVO("str0ng!pass")

    def test_raises_when_missing_lowercase(self) -> None:
        with pytest.raises(InvalidStaffMemberPassword):
            StaffMemberPasswordVO("STR0NG!PASS")

    def test_raises_when_missing_digit(self) -> None:
        with pytest.raises(InvalidStaffMemberPassword):
            StaffMemberPasswordVO("Strong!Pass")

    def test_raises_when_missing_special_character(self) -> None:
        with pytest.raises(InvalidStaffMemberPassword):
            StaffMemberPasswordVO("Str0ngPass")

    def test_raises_when_shorter_than_min_length(self) -> None:
        with pytest.raises(InvalidString):
            StaffMemberPasswordVO("S1!aB2c")

    def test_raises_when_longer_than_max_length(self) -> None:
        with pytest.raises(InvalidString):
            StaffMemberPasswordVO("Str0ng!Pass" * 5)
