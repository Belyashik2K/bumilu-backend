import pytest
from app.core.domain.value_objects.string.exceptions import InvalidString
from app.modules.places.domain.places.value_objects.phone_number.exceptions import (
    InvalidPlacePhoneNumber,
)
from app.modules.places.domain.places.value_objects.phone_number.object import (
    PlacePhoneNumberVO,
)


class TestPlacePhoneNumberVO:
    @pytest.mark.parametrize(
        "raw",
        [
            "+7 (999) 123-45-67",
            "89991234567",
            "79991234567",
        ],
    )
    def test_normalizes_valid_number_to_plus_seven_format(self, raw: str) -> None:
        phone = PlacePhoneNumberVO(raw)

        assert phone.value == "+79991234567"

    def test_raises_when_digit_count_is_not_eleven(self) -> None:
        with pytest.raises(InvalidPlacePhoneNumber):
            PlacePhoneNumberVO("+7999123456")

    def test_raises_when_number_does_not_start_with_seven_or_eight(self) -> None:
        with pytest.raises(InvalidPlacePhoneNumber):
            PlacePhoneNumberVO("99991234567")

    def test_raises_on_letters_via_base_pattern_check(self) -> None:
        with pytest.raises(InvalidString):
            PlacePhoneNumberVO("abc-999-1234")
