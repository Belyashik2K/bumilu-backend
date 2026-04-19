from dataclasses import dataclass

from app.modules.places.domain.categories.value_objects.marker_color.exceptions import (
    InvalidMarkerColor,
)


@dataclass(frozen=True, slots=True)
class PlaceCategoryMarkerColorVO:
    value: str

    def __post_init__(self):
        if not self.value.startswith("#") or len(self.value) != 7:
            raise InvalidMarkerColor(
                color=self.value,
            )

    @property
    def rgb(self) -> tuple[int, ...]:
        hex_code = self.value.lstrip("#")
        return tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))
