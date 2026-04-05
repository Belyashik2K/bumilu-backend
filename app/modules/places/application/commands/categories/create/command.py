from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatePlaceCategoryCommand:
    slug: str
    icon_key: str
    marker_color: str
