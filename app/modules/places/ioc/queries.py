from dishka import (
    Provider,
    Scope,
    provide,
)

from app.modules.places.application.interfaces.file_storage_url_builder import (
    IFileStorageURLBuilder,
)
from app.modules.places.application.interfaces.readers.place import (
    IPlaceReader,
)
from app.modules.places.application.interfaces.readers.place_translation import (
    IPlaceTranslationReader,
)
from app.modules.places.application.queries.categories.admin.get.handler import (
    GetAdminPlaceCategoryQueryHandler,
)
from app.modules.places.application.queries.categories.admin.get_all.handler import (
    GetAdminPlaceCategoriesListQueryHandler,
)
from app.modules.places.application.queries.categories.admin.get_all_translations.handler import (
    GetAdminPlaceCategoryTranslationsListQueryHandler,
)
from app.modules.places.application.queries.categories.admin.get_translation.handler import (
    GetAdminPlaceCategoryTranslationQueryHandler,
)
from app.modules.places.application.queries.categories.shared.readers.place_category import (
    IPlaceCategoryReader,
)
from app.modules.places.application.queries.categories.shared.readers.place_category_translation import (
    IPlaceCategoryTranslationReader,
)
from app.modules.places.application.queries.categories.user.get_all.handler import (
    GetAllPlaceCategoriesQueryHandler,
)
from app.modules.places.application.queries.places.admin.get.handler import (
    GetAdminPlaceQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_all.handler import (
    GetAdminPlacesListQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_map_poi.handler import (
    GetAdminPlacesMapPOIQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_phones.handler import (
    GetAdminPlacePhonesQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_photos.handler import (
    GetAdminPlacePhotosQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_translation_by_language_code.handler import (
    GetAdminPlaceTranslationByLanguageCodeQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_translations.handler import (
    GetAdminPlaceTranslationsQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_working_day_by_weekday.handler import (
    GetAdminPlaceWorkingDayByWeekdayQueryHandler,
)
from app.modules.places.application.queries.places.admin.get_working_days.handler import (
    GetAdminPlaceWorkingDaysQueryHandler,
)
from app.modules.places.application.queries.places.user.get.handler import (
    GetPlaceQueryHandler,
)
from app.modules.places.application.queries.places.user.get_all.handler import (
    GetAllPlacesQueryHandler,
)
from app.modules.places.application.queries.places.user.get_map_poi.handler import (
    GetPlacesMapPOIQueryHandler,
)


class PlacesQueryHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_all_place_categories_handler(
        self, place_category_reader: IPlaceCategoryReader
    ) -> GetAllPlaceCategoriesQueryHandler:
        return GetAllPlaceCategoriesQueryHandler(
            place_category_reader=place_category_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_place_handler(
        self, place_reader: IPlaceReader, storage_url_builder: IFileStorageURLBuilder
    ) -> GetPlaceQueryHandler:
        return GetPlaceQueryHandler(
            place_reader=place_reader,
            storage_url_builder=storage_url_builder,
        )

    @provide(scope=Scope.REQUEST)
    async def get_all_places_handler(
        self, place_reader: IPlaceReader, storage_url_builder: IFileStorageURLBuilder
    ) -> GetAllPlacesQueryHandler:
        return GetAllPlacesQueryHandler(
            place_reader=place_reader,
            storage_url_builder=storage_url_builder,
        )

    @provide(scope=Scope.REQUEST)
    async def get_places_map_poi_handler(
        self, place_reader: IPlaceReader
    ) -> GetPlacesMapPOIQueryHandler:
        return GetPlacesMapPOIQueryHandler(
            place_reader=place_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_admin_place_categories_handler(
        self, place_category_reader: IPlaceCategoryReader
    ) -> GetAdminPlaceCategoriesListQueryHandler:
        return GetAdminPlaceCategoriesListQueryHandler(
            place_category_reader=place_category_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_admin_place_category_handler(
        self, place_category_reader: IPlaceCategoryReader
    ) -> GetAdminPlaceCategoryQueryHandler:
        return GetAdminPlaceCategoryQueryHandler(
            place_category_reader=place_category_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_admin_place_category_translations_handler(
        self, place_category_translation_reader: IPlaceCategoryTranslationReader
    ) -> GetAdminPlaceCategoryTranslationsListQueryHandler:
        return GetAdminPlaceCategoryTranslationsListQueryHandler(
            place_category_translation_reader=place_category_translation_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_admin_place_category_translation_handler(
        self, place_category_translation_reader: IPlaceCategoryTranslationReader
    ) -> GetAdminPlaceCategoryTranslationQueryHandler:
        return GetAdminPlaceCategoryTranslationQueryHandler(
            place_category_translation_reader=place_category_translation_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_admin_place_working_day_by_weekday_handler(
        self, place_reader: IPlaceReader
    ) -> GetAdminPlaceWorkingDayByWeekdayQueryHandler:
        return GetAdminPlaceWorkingDayByWeekdayQueryHandler(
            place_reader=place_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_admin_place_working_days_handler(
        self, place_reader: IPlaceReader
    ) -> GetAdminPlaceWorkingDaysQueryHandler:
        return GetAdminPlaceWorkingDaysQueryHandler(
            place_reader=place_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_admin_place_photos_handler(
        self, place_reader: IPlaceReader, storage_url_builder: IFileStorageURLBuilder
    ) -> GetAdminPlacePhotosQueryHandler:
        return GetAdminPlacePhotosQueryHandler(
            place_reader=place_reader,
            storage_url_builder=storage_url_builder,
        )

    @provide(scope=Scope.REQUEST)
    async def get_admin_place_phones_handler(
        self, place_reader: IPlaceReader
    ) -> GetAdminPlacePhonesQueryHandler:
        return GetAdminPlacePhonesQueryHandler(
            place_reader=place_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_admin_place_translations_handler(
        self, place_translation_reader: IPlaceTranslationReader
    ) -> GetAdminPlaceTranslationsQueryHandler:
        return GetAdminPlaceTranslationsQueryHandler(
            place_translation_reader=place_translation_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_admin_place_translation_handler(
        self, place_translation_reader: IPlaceTranslationReader
    ) -> GetAdminPlaceTranslationByLanguageCodeQueryHandler:
        return GetAdminPlaceTranslationByLanguageCodeQueryHandler(
            place_translation_reader=place_translation_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_admin_place_details_handler(
        self,
        place_reader: IPlaceReader,
    ) -> GetAdminPlaceQueryHandler:
        return GetAdminPlaceQueryHandler(
            place_reader=place_reader,
        )

    @provide(scope=Scope.REQUEST)
    async def get_admin_places_list_handler(
        self,
        place_reader: IPlaceReader,
    ) -> GetAdminPlacesListQueryHandler:
        return GetAdminPlacesListQueryHandler(place_reader=place_reader)

    @provide(scope=Scope.REQUEST)
    async def get_admin_place_map_poi_handler(
        self, place_reader: IPlaceReader
    ) -> GetAdminPlacesMapPOIQueryHandler:
        return GetAdminPlacesMapPOIQueryHandler(
            place_reader=place_reader,
        )
