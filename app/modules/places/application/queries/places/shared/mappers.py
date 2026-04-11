from app.modules.places.application.queries.categories.shared.mappers import (
    PlaceCategoryMapper,
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
from app.modules.places.application.queries.places.shared.models.place_photo import (
    PlacePhotoReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_rating import (
    PlaceRatingReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_user_context import (
    PlaceUserContextReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_working_day import (
    PlaceWorkingDayReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_working_hour import (
    PlaceWorkingHourReadModel,
)
from app.modules.places.infrastructure.database.models import (
    PlaceModel,
)


class PlaceReadModelMapper:
    @staticmethod
    def map_user_context(
        is_favorite: bool,
    ) -> PlaceUserContextReadModel:
        return PlaceUserContextReadModel(
            is_favorite=is_favorite,
        )

    @staticmethod
    def map_location(place: PlaceModel) -> PlaceLocationReadModel:
        return PlaceLocationReadModel(
            latitude=place.latitude,
            longitude=place.longitude,
        )

    @staticmethod
    def map_working_days(
        place: PlaceModel,
    ) -> list[PlaceWorkingDayReadModel]:
        return [
            PlaceWorkingDayReadModel(
                weekday=wd.weekday,
                status=wd.status,
                intervals=[
                    PlaceWorkingHourReadModel(
                        start=wh.start_time,
                        end=wh.end_time,
                    )
                    for wh in wd.working_hours
                ],
            )
            for wd in place.working_days
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

    @classmethod
    def map_address(cls, place: PlaceModel) -> PlaceAddressReadModel:
        translation = place.translations[0]

        return PlaceAddressReadModel(
            display=translation.address_display,
            taxi=place.address_taxi,
            taxi_comment=place.address_taxi_comment,
        )

    @classmethod
    def map_details(
        cls,
        place: PlaceModel,
        is_favorite: bool,
    ) -> PlaceDetailsReadModel:
        translation = place.translations[0]

        return PlaceDetailsReadModel(
            id=place.id,
            title=translation.title,
            description=translation.description,
            short_description=translation.short_description,
            timezone=place.timezone,
            category=PlaceCategoryMapper.map_localized_category(place.category),
            photos=cls.map_photos(place),
            location=cls.map_location(place),
            address=cls.map_address(place),
            rating=cls.map_rating(
                average=place.rating_average,
                reviews_count=place.rating_reviews_count,
            ),
            phones=cls.map_phones(place),
            working_days=cls.map_working_days(place),
            user_context=cls.map_user_context(is_favorite=is_favorite),
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
            category=PlaceCategoryMapper.map_localized_category(place.category),
            photos=cls.map_photos(place),
            location=cls.map_location(place),
            rating=cls.map_rating(
                average=rating_average,
                reviews_count=reviews_count,
            ),
            working_days=cls.map_working_days(place),
        )

    @classmethod
    def map_poi(cls, place: PlaceModel) -> PlaceMapPOIReadModel:
        translation = place.translations[0]

        return PlaceMapPOIReadModel(
            id=place.id,
            title=translation.title,
            category=PlaceCategoryMapper.map_localized_category(place.category),
            location=cls.map_location(place),
        )

    @classmethod
    def map_photos(cls, place: PlaceModel) -> list[PlacePhotoReadModel]:
        photo_url = "https://media.bumilu.ru/banner.jpg"  # TODO: add real photo url from place.photos
        thumbnail_url = "https://media.bumilu.ru/banner_thumbnail.jpg"

        return [PlacePhotoReadModel(url=photo_url, thumbnail_url=thumbnail_url)] * 5
