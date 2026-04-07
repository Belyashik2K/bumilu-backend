from polyline import polyline

from app.core.enums import LanguageEnum
from app.modules.routing.application.interfaces.routing_gateway import IRoutingGateway
from app.modules.routing.application.models.route_bounds import RouteBounds
from app.modules.routing.application.models.route_geometry import RouteGeometry
from app.modules.routing.application.models.route_instruction import RouteInstruction
from app.modules.routing.application.models.route_leg import RouteLeg
from app.modules.routing.application.models.route_path import RoutePath
from app.modules.routing.application.queries.get_route.query import Waypoint
from app.modules.routing.infrastructure.valhalla.client import ValhallaClient
from app.modules.routing.shared.enums.route_geometry_format import (
    RouteGeometryFormatEnum,
)
from app.modules.routing.shared.enums.travel_mode import TravelModeEnum


class ValhallaRoutingGateway(IRoutingGateway):
    def __init__(
        self,
        client: ValhallaClient,
    ) -> None:
        self._client = client

    async def get_route(
        self,
        points: list[Waypoint],
        mode: TravelModeEnum,
        translation_language: LanguageEnum,
    ) -> RoutePath:
        if len(points) < 2:
            raise ValueError("At least 2 waypoints are required")

        response = await self._client.route(
            locations=[
                {
                    "lat": point.latitude,
                    "lon": point.longitude,
                    "type": "break",
                }
                for point in points
            ],
            costing=self._map_costing(mode),
            language=self._map_translation_language(translation_language),
        )

        trip = response["trip"]
        trip_summary = trip["summary"]
        leg_payloads = trip.get("legs", [])

        if not leg_payloads:
            raise ValueError("Valhalla returned route without legs")

        legs = tuple(
            self._map_leg(leg_payload=leg_payload, mode=mode)
            for leg_payload in leg_payloads
        )

        return RoutePath(
            mode=mode,
            distance_meters=self._kilometers_to_meters(trip_summary["length"]),
            duration_seconds=self._seconds_to_int(trip_summary["time"]),
            geometry=self._build_route_geometry(leg_payloads),
            bounds=RouteBounds(
                north=trip_summary["max_lat"],
                south=trip_summary["min_lat"],
                east=trip_summary["max_lon"],
                west=trip_summary["min_lon"],
            ),
            legs=legs,
        )

    @staticmethod
    def _map_costing(mode: TravelModeEnum) -> str:
        match mode:
            case TravelModeEnum.WALK:
                return "pedestrian"
            case TravelModeEnum.DRIVE:
                return "auto"
            case _:
                raise ValueError(f"Unsupported travel mode: {mode}")

    @staticmethod
    def _map_translation_language(language: LanguageEnum) -> str:
        match language:
            case LanguageEnum.RU:
                return "ru-RU"
            case LanguageEnum.EN:
                return "en-US"
            case LanguageEnum.ZH:
                return "zh-CN"
            case _:
                raise ValueError(f"Unsupported translation language: {language}")

    def _map_leg(
        self,
        leg_payload: dict,
        mode: TravelModeEnum,
    ) -> RouteLeg:
        summary = leg_payload["summary"]
        maneuvers = leg_payload.get("maneuvers", [])

        return RouteLeg(
            distance_meters=self._kilometers_to_meters(summary["length"]),
            duration_seconds=self._seconds_to_int(summary["time"]),
            geometry=RouteGeometry(
                format=RouteGeometryFormatEnum.POLYLINE6,
                encoded=leg_payload["shape"],
            ),
            instructions=tuple(
                self._map_instruction(
                    maneuver_payload=maneuver,
                    default_mode=mode,
                )
                for maneuver in maneuvers
            ),
        )

    def _map_instruction(
        self,
        maneuver_payload: dict,
        default_mode: TravelModeEnum,
    ) -> RouteInstruction:
        return RouteInstruction(
            text=maneuver_payload["instruction"],
            distance_meters=self._kilometers_to_meters(maneuver_payload["length"]),
            duration_seconds=self._seconds_to_int(maneuver_payload["time"]),
            begin_shape_index=int(maneuver_payload["begin_shape_index"]),
            end_shape_index=int(maneuver_payload["end_shape_index"]),
            maneuver_type=str(maneuver_payload["type"]),
            travel_mode=self._map_travel_mode(
                maneuver_payload.get("travel_mode"),
                default=default_mode,
            ),
            bearing_before=self._optional_int(maneuver_payload.get("bearing_before")),
            bearing_after=self._optional_int(maneuver_payload.get("bearing_after")),
        )

    @staticmethod
    def _build_route_geometry(legs_payload: list[dict]) -> RouteGeometry:
        merged_coordinates: list[tuple[float, float]] = []

        for leg_payload in legs_payload:
            encoded_shape = leg_payload.get("shape")
            if not encoded_shape:
                continue

            coordinates = polyline.decode(encoded_shape, precision=6)
            if not coordinates:
                continue

            if not merged_coordinates:
                merged_coordinates.extend(coordinates)
                continue

            if ValhallaRoutingGateway._same_coordinate(
                merged_coordinates[-1],
                coordinates[0],
            ):
                merged_coordinates.extend(coordinates[1:])
            else:
                merged_coordinates.extend(coordinates)

        if not merged_coordinates:
            raise ValueError("Valhalla returned empty route geometry")

        return RouteGeometry(
            format=RouteGeometryFormatEnum.POLYLINE6,
            encoded=polyline.encode(merged_coordinates, precision=6),
        )

    @staticmethod
    def _same_coordinate(
        left: tuple[float, float],
        right: tuple[float, float],
        epsilon: float = 1e-6,
    ) -> bool:
        return abs(left[0] - right[0]) <= epsilon and abs(left[1] - right[1]) <= epsilon

    @staticmethod
    def _map_travel_mode(
        raw_mode: str | None,
        default: TravelModeEnum,
    ) -> TravelModeEnum:
        if raw_mode == "pedestrian":
            return TravelModeEnum.WALK
        if raw_mode == "drive":
            return TravelModeEnum.DRIVE
        if raw_mode == "auto":
            return TravelModeEnum.DRIVE
        return default

    @staticmethod
    def _kilometers_to_meters(value: float | int) -> int:
        return int(round(float(value) * 1000))

    @staticmethod
    def _seconds_to_int(value: float | int) -> int:
        return int(round(float(value)))

    @staticmethod
    def _optional_int(value: int | float | None) -> int | None:
        if value is None:
            return None
        return int(round(float(value)))
