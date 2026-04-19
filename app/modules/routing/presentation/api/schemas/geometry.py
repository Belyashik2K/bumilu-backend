from pydantic import (
    BaseModel,
    Field,
)

from app.modules.routing.shared.enums.route_geometry_format import (
    RouteGeometryFormatEnum,
)


class RouteGeometrySchema(BaseModel):
    format: RouteGeometryFormatEnum = Field(
        ...,
        description="Format of the route geometry encoding.",
        examples=[RouteGeometryFormatEnum.POLYLINE6],
    )
    encoded: str = Field(
        ...,
        description="Encoded route geometry string.",
        examples=["_p~iF~ps|U_ulLnnqC_mqNvxq`@"],
    )
