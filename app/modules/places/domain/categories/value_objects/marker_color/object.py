from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class PlaceCategoryMarkerColorVO:
    hex_code: str

    def __post_init__(self):
        if not self.hex_code.startswith("#") or len(self.hex_code) != 7:
            raise ValueError(f"Invalid hex code: {self.hex_code}")

    @property
    def rgb(self) -> tuple[int, ...]:
        hex_code = self.hex_code.lstrip("#")
        return tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))
