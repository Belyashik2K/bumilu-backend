import pytest
from app.core.domain.value_objects.location.exceptions import (
    InvalidLatitude,
    InvalidLongitude,
)
from app.core.domain.value_objects.location.object import LocationVO


class TestLocationVOConstruction:
    def test_accepts_valid_coordinates(self) -> None:
        location = LocationVO(latitude=59.9311, longitude=30.3609)

        assert location.latitude == 59.9311
        assert location.longitude == 30.3609

    @pytest.mark.parametrize("latitude", [-90.0, 90.0])
    def test_accepts_boundary_latitude(self, latitude: float) -> None:
        location = LocationVO(latitude=latitude, longitude=0.0)

        assert location.latitude == latitude

    @pytest.mark.parametrize("longitude", [-180.0, 180.0])
    def test_accepts_boundary_longitude(self, longitude: float) -> None:
        location = LocationVO(latitude=0.0, longitude=longitude)

        assert location.longitude == longitude

    @pytest.mark.parametrize("latitude", [-90.0001, 90.0001, -1000.0, 1000.0])
    def test_raises_when_latitude_out_of_range(self, latitude: float) -> None:
        with pytest.raises(InvalidLatitude):
            LocationVO(latitude=latitude, longitude=0.0)

    @pytest.mark.parametrize("longitude", [-180.0001, 180.0001, -1000.0, 1000.0])
    def test_raises_when_longitude_out_of_range(self, longitude: float) -> None:
        with pytest.raises(InvalidLongitude):
            LocationVO(latitude=0.0, longitude=longitude)

    def test_raises_when_latitude_is_none(self) -> None:
        with pytest.raises(InvalidLatitude):
            LocationVO(latitude=None, longitude=0.0)  # type: ignore[arg-type]

    def test_raises_when_longitude_is_none(self) -> None:
        with pytest.raises(InvalidLongitude):
            LocationVO(latitude=0.0, longitude=None)  # type: ignore[arg-type]


class TestLocationVOFromCoordinates:
    def test_returns_instance_for_valid_coordinates(self) -> None:
        location = LocationVO.from_coordinates(latitude=59.9311, longitude=30.3609)

        assert location == LocationVO(latitude=59.9311, longitude=30.3609)

    def test_returns_none_when_latitude_is_none(self) -> None:
        location = LocationVO.from_coordinates(latitude=None, longitude=30.3609)

        assert location is None

    def test_returns_none_when_longitude_is_none(self) -> None:
        location = LocationVO.from_coordinates(latitude=59.9311, longitude=None)

        assert location is None

    def test_returns_none_when_both_are_none(self) -> None:
        location = LocationVO.from_coordinates(latitude=None, longitude=None)

        assert location is None

    def test_raises_when_coordinates_out_of_range(self) -> None:
        with pytest.raises(InvalidLatitude):
            LocationVO.from_coordinates(latitude=91.0, longitude=30.3609)
