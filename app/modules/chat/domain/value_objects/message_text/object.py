from dataclasses import dataclass

MAX_PREVIEW_LENGTH = 32


@dataclass(frozen=True, slots=True, kw_only=True)
class MessageTextVO:
    value: str

    def __post_init__(self) -> None: ...

    def _length(self) -> int:
        return len(self.value)

    @property
    def preview(self) -> str:
        if self._length() <= MAX_PREVIEW_LENGTH:
            return self.value
        return f"{self.value[:32]}..."
