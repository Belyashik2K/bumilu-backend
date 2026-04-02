from app.modules.places.application.queries.categories.shared.models.place_category import (
    LocalizedPlaceCategoryReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_address import (
    PlaceAddressReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_card import (
    PlaceCardReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_details import (
    PlaceDetailsReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_location import (
    PlaceLocationReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_map_poi import (
    PlaceMapPOIReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_phone import (
    PlacePhoneReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_rating import (
    PlaceRatingReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_working_hour import (
    PlaceWorkingHourReadModel,
)
from app.modules.places.infrastructure.database.models import (
    PlaceCategoryModel,
    PlaceModel,
)


class PlaceReadModelMapper:
    @staticmethod
    def map_location(place: PlaceModel) -> PlaceLocationReadModel:
        return PlaceLocationReadModel(
            latitude=place.latitude,
            longitude=place.longitude,
        )

    @staticmethod
    def map_working_hours(
        place: PlaceModel,
    ) -> list[PlaceWorkingHourReadModel]:
        return [
            PlaceWorkingHourReadModel(
                weekday=wh.weekday,
                start_time=wh.start_time,
                end_time=wh.end_time,
            )
            for wh in place.working_hours
        ]

    @staticmethod
    def map_phones(place: PlaceModel) -> list[PlacePhoneReadModel]:
        return [
            PlacePhoneReadModel(
                number=phone.number,
                type=phone.type,
                primary=phone.is_primary,
            )
            for phone in place.phones
        ]

    @staticmethod
    def map_rating(
        *,
        average: float | None,
        reviews_count: int,
    ) -> PlaceRatingReadModel:
        return PlaceRatingReadModel(
            average=average,
            reviews_count=reviews_count,
        )

    @staticmethod
    def map_localized_category(
        category: PlaceCategoryModel,
    ) -> LocalizedPlaceCategoryReadModel:
        translation = category.translations[0]
        return LocalizedPlaceCategoryReadModel(
            id=category.id,
            slug=category.slug,
            name=translation.name,
            icon_key=category.icon_key,
            marker_color=category.marker_color,
        )

    @classmethod
    def map_address(cls, place: PlaceModel) -> PlaceAddressReadModel:
        translation = place.translations[0]

        return PlaceAddressReadModel(
            display=translation.address_display,
            taxi=place.address_taxi,
            taxi_comment=place.address_taxi_comment,
        )

    @classmethod
    def map_details(cls, place: PlaceModel) -> PlaceDetailsReadModel:
        translation = place.translations[0]

        return PlaceDetailsReadModel(
            id=place.id,
            category_id=place.category_id,
            title=translation.title,
            description=translation.description,
            short_description=translation.short_description,
            timezone=place.timezone,
            location=cls.map_location(place),
            address=cls.map_address(place),
            rating=cls.map_rating(
                average=place.rating_average,
                reviews_count=place.rating_reviews_count,
            ),
            phones=cls.map_phones(place),
            working_hours=cls.map_working_hours(place),
        )

    @classmethod
    def map_card(
        cls,
        place: PlaceModel,
        *,
        rating_average: float | None,
        reviews_count: int,
    ) -> PlaceCardReadModel:
        translation = place.translations[0]

        return PlaceCardReadModel(
            id=place.id,
            title=translation.title,
            short_description=translation.short_description,
            timezone=place.timezone,
            category=cls.map_localized_category(place.category),
            location=cls.map_location(place),
            rating=cls.map_rating(
                average=rating_average,
                reviews_count=reviews_count,
            ),
            working_hours=cls.map_working_hours(place),
        )

    @classmethod
    def map_poi(cls, place: PlaceModel) -> PlaceMapPOIReadModel:
        translation = place.translations[0]

        return PlaceMapPOIReadModel(
            id=place.id,
            title=translation.title,
            category=cls.map_localized_category(place.category),
            location=cls.map_location(place),
        )
