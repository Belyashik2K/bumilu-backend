from datetime import time
from zoneinfo import ZoneInfo

from app.core.utils import get_current_dt
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
from app.modules.places.application.queries.places.shared.models.place_llm_context import (
    NearbyPlaceLLMContextReadModel,
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
from app.modules.places.shared.enums.place_working_day_status import (
    PlaceWorkingDayStatusEnum,
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
        taxi: str | None,
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
    @classmethod
    def map_to_llm_context(
        cls,
        *,
        place: PlaceModel,
        rating_average: float | None = None,
        reviews_count: int,
        distance_meters: float | None = None,
    ) -> NearbyPlaceLLMContextReadModel:
        translation = place.translations[0]

        assert (
            translation.short_description is not None
        ), "translation.short_description must be set"
        assert (
            translation.address_display is not None
        ), "translation.address_display must be set"
        assert place.address_taxi is not None, "place.address_taxi must be set"

        return NearbyPlaceLLMContextReadModel(
            id=place.id,
            title=translation.title,
            short_description=translation.short_description,
            category_title=place.category.translations[0].name,
            address=PlaceAddressMapper.map(
                display=translation.address_display,
                taxi=place.address_taxi,
                taxi_comment=place.address_taxi_comment,
            ),
            rating=cls.map_rating(
                average=rating_average,
                reviews_count=reviews_count,
            ),
            distance_meters=int(distance_meters)
            if distance_meters is not None
            else None,
            is_open_now=cls._is_open_now(place=place),
        )

    @staticmethod
    def _is_open_now(place: PlaceModel) -> bool | None:
        if not place.working_days:
            return None

        now = get_current_dt().astimezone(ZoneInfo(place.timezone))
        current_weekday = now.isoweekday()
        current_time = now.time()

        working_day = next(
            (day for day in place.working_days if day.weekday == current_weekday),
            None,
        )

        if working_day is None:
            return None

        if working_day.status == PlaceWorkingDayStatusEnum.UNSPECIFIED:
            return None

        if working_day.status == PlaceWorkingDayStatusEnum.CLOSED:
            return False

        if working_day.status == PlaceWorkingDayStatusEnum.ALL_DAY:
            return True

        if not working_day.working_hours:
            return False

        return any(
            PlaceReadModelMapper._is_time_in_range(
                current_time=current_time,
                time_from=working_hour.start_time,
                time_to=working_hour.end_time,
            )
            for working_hour in working_day.working_hours
        )

    @staticmethod
    def _is_time_in_range(
        *,
        current_time: time,
        time_from: time,
        time_to: time,
    ) -> bool:
        if time_from <= time_to:
            return time_from <= current_time <= time_to

        return current_time >= time_from or current_time <= time_to

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

        assert (
            translation.address_display is not None
        ), "translation.address_display must be set"
        assert place.address_taxi is not None, "place.address_taxi must be set"

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
        translation: PlaceTranslationModel | None = None,
    ) -> AdminPlaceDetailsReadModel:
        return AdminPlaceDetailsReadModel(
            id=place.id,
            title=translation.title if translation is not None else None,
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
