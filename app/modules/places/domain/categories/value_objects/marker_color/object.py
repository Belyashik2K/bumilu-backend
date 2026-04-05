from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlaceCategoryMarkerColorVO:
    value: str

    def __post_init__(self):
        if not self.value.startswith("#") or len(self.value) != 7:
            raise ValueError(f"Invalid hex code: {self.value}")

    @property
    def rgb(self) -> tuple[int, ...]:
        hex_code = self.value.lstrip("#")
        return tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))
