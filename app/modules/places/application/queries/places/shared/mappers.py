from app.modules.places.application.queries.categories.shared.mappers import (
    PlaceCategoryMapper,
)
from app.modules.places.application.queries.places.shared.models.place_address import (
    AdminPlaceAddressReadModel,
    PlaceAddressReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_card import (
    AdminPlaceCardReadModel,
    PlaceCardReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_details import (
    AdminPlaceDetailsReadModel,
    PlaceDetailsReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_location import (
    PlaceLocationReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_map_poi import (
    AdminPlaceMapPOIReadModel,
    PlaceMapPOIReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_phone import (
    AdminPlacePhoneReadModel,
    PlacePhoneReadModel,
)
from app.modules.places.application.queries.places.shared.models.place_photo import (
    AdminPlacePhotoReadModel,
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
    PlacePhoneModel,
    PlacePhotoModel,
    PlaceTranslationModel,
    PlaceWorkingDayModel,
)


class PlaceWorkingDayMapper:
    @staticmethod
    def map(working_day: PlaceWorkingDayModel) -> PlaceWorkingDayReadModel:
        return PlaceWorkingDayReadModel(
            weekday=working_day.weekday,
            status=working_day.status,
            intervals=[
                PlaceWorkingHourReadModel(
                    start=wh.start_time,
                    end=wh.end_time,
                )
                for wh in working_day.working_hours
            ],
        )


class PlacePhoneMapper:
    @staticmethod
    def map(phone: PlacePhoneModel) -> PlacePhoneReadModel:
        return PlacePhoneReadModel(
            number=phone.number,
            type=phone.type,
            primary=phone.is_primary,
        )

    @staticmethod
    def map_admin(phone: PlacePhoneModel) -> AdminPlacePhoneReadModel:
        return AdminPlacePhoneReadModel(
            number=phone.number,
            type=phone.type,
            primary=phone.is_primary,
            id=phone.id,
        )


class PlaceUserContextMapper:
    @staticmethod
    def map(
        is_favorite: bool,
    ) -> PlaceUserContextReadModel:
        return PlaceUserContextReadModel(
            is_favorite=is_favorite,
        )


class PlacePhotoMapper:
    @staticmethod
    def map(photo: PlacePhotoModel) -> PlacePhotoReadModel:
        return PlacePhotoReadModel(
            file_key=photo.file_key,
            thumbnail_file_key=photo.thumbnail_file_key,
        )

    @staticmethod
    def map_admin(photo: PlacePhotoModel) -> AdminPlacePhotoReadModel:
        return AdminPlacePhotoReadModel(
            id=photo.id,
            file_key=photo.file_key,
            thumbnail_file_key=photo.thumbnail_file_key,
            status=photo.status,
        )


class PlaceAddressMapper:
    @staticmethod
    def map(
        display: str,
        taxi: str,
        taxi_comment: str | None,
    ) -> PlaceAddressReadModel:
        return PlaceAddressReadModel(
            display=display,
            taxi=taxi,
            taxi_comment=taxi_comment,
        )

    @staticmethod
    def map_admin(
        taxi: str,
        taxi_comment: str | None,
    ) -> AdminPlaceAddressReadModel:
        return AdminPlaceAddressReadModel(
            taxi=taxi,
            taxi_comment=taxi_comment,
        )


class PlaceMapPOIMapper:
    @staticmethod
    def map(place: PlaceModel) -> PlaceMapPOIReadModel:
        translation = place.translations[0]

        return PlaceMapPOIReadModel(
            id=place.id,
            title=translation.title,
            category=PlaceCategoryMapper.map_localized_category(place.category),
            location=PlaceReadModelMapper.map_location(place),
        )

    @staticmethod
    def map_admin(
        place: PlaceModel,
        translation: PlaceTranslationModel | None = None,
    ) -> AdminPlaceMapPOIReadModel:
        return AdminPlaceMapPOIReadModel(
            id=place.id,
            title=translation.title if translation is not None else None,
            category=PlaceCategoryMapper.map_category(place.category),
            location=PlaceReadModelMapper.map_location(place),
        )


class PlaceReadModelMapper:
    @staticmethod
    def map_location(place: PlaceModel) -> PlaceLocationReadModel:
        return PlaceLocationReadModel(
            latitude=place.latitude,
            longitude=place.longitude,
        )

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
            photos=[PlacePhotoMapper.map(photo) for photo in place.photos],
            location=cls.map_location(place),
            address=PlaceAddressMapper.map(
                display=translation.address_display,
                taxi=place.address_taxi,
                taxi_comment=place.address_taxi_comment,
            ),
            rating=cls.map_rating(
                average=place.rating_average,
                reviews_count=place.rating_reviews_count,
            ),
            phones=[PlacePhoneMapper.map(phone) for phone in place.phones],
            working_days=[
                PlaceWorkingDayMapper.map(working_day)
                for working_day in place.working_days
            ],
            user_context=PlaceUserContextMapper.map(is_favorite=is_favorite),
        )

    @classmethod
    def map_admin_details(
        cls,
        place: PlaceModel,
    ) -> AdminPlaceDetailsReadModel:
        return AdminPlaceDetailsReadModel(
            id=place.id,
            timezone=place.timezone,
            category=PlaceCategoryMapper.map_category(place.category),
            location=cls.map_location(place),
            address=PlaceAddressMapper.map_admin(
                taxi=place.address_taxi,
                taxi_comment=place.address_taxi_comment,
            ),
            rating=cls.map_rating(
                average=place.rating_average,
                reviews_count=place.rating_reviews_count,
            ),
            status=place.status,
            created_at=place.created_at,
            updated_at=place.updated_at,
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
            photos=[PlacePhotoMapper.map(photo) for photo in place.photos],
            location=cls.map_location(place),
            rating=cls.map_rating(
                average=rating_average,
                reviews_count=reviews_count,
            ),
            working_days=[
                PlaceWorkingDayMapper.map(working_day)
                for working_day in place.working_days
            ],
        )

    @classmethod
    def map_admin_card(
        cls,
        place: PlaceModel,
        translation: PlaceTranslationModel | None = None,
        *,
        rating_average: float | None,
        reviews_count: int,
    ) -> AdminPlaceCardReadModel:
        return AdminPlaceCardReadModel(
            id=place.id,
            title=translation.title if translation is not None else None,
            timezone=place.timezone,
            address=PlaceAddressMapper.map_admin(
                taxi=place.address_taxi,
                taxi_comment=place.address_taxi_comment,
            ),
            category=PlaceCategoryMapper.map_category(place.category),
            location=cls.map_location(place),
            rating=cls.map_rating(average=rating_average, reviews_count=reviews_count),
            created_at=place.created_at,
            updated_at=place.updated_at,
            status=place.status,
        )
