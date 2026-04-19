from dataclasses import dataclass

from app.modules.routing.shared.enums.route_geometry_format import (
    RouteGeometryFormatEnum,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class RouteGeometry:
    format: RouteGeometryFormatEnum
    encoded: str
