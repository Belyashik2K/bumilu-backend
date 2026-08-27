from app.modules.auth.infrastructure.hashers.pwdlib_staff_password_hasher import (
    PWDLibStaffPasswordHasher,
)


class TestPWDLibStaffPasswordHasher:
    def test_hash_does_not_return_the_plaintext_password(self) -> None:
        hasher = PWDLibStaffPasswordHasher()

        hashed = hasher.hash("Str0ng!Pass")

        assert hashed != "Str0ng!Pass"

    def test_hash_is_salted_and_differs_between_calls(self) -> None:
        hasher = PWDLibStaffPasswordHasher()

        first = hasher.hash("Str0ng!Pass")
        second = hasher.hash("Str0ng!Pass")

        assert first != second

    def test_verify_succeeds_for_correct_password(self) -> None:
        hasher = PWDLibStaffPasswordHasher()
        hashed = hasher.hash("Str0ng!Pass")

        assert hasher.verify("Str0ng!Pass", hashed) is True

    def test_verify_fails_for_incorrect_password(self) -> None:
        hasher = PWDLibStaffPasswordHasher()
        hashed = hasher.hash("Str0ng!Pass")

        assert hasher.verify("Wr0ng!Pass", hashed) is False

    def test_verify_succeeds_across_two_independently_produced_hashes(self) -> None:
        hasher = PWDLibStaffPasswordHasher()
        first_hash = hasher.hash("Str0ng!Pass")
        second_hash = hasher.hash("Str0ng!Pass")

        assert hasher.verify("Str0ng!Pass", first_hash) is True
        assert hasher.verify("Str0ng!Pass", second_hash) is True
