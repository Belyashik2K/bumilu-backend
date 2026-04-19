from app.core.application.queries import IQueryHandler
from app.modules.routes.application.exceptions.route import (
    RouteNotFound,
    RouteTranslationNotFound,
)
from app.modules.routes.application.interfaces.readers.route import IRouteReader
from app.modules.routes.application.interfaces.readers.route_translation import (
    IRouteTranslationReader,
)
from app.modules.routes.application.queries.admin.get_translation_by_language_code.query import (
    GetAdminRouteTranslationByLanguageCodeQuery,
)
from app.modules.routes.application.queries.shared.models.route_translation import (
    RouteTranslationReadModel,
)


class GetAdminRouteTranslationByLanguageCodeQueryHandler(
    IQueryHandler[
        GetAdminRouteTranslationByLanguageCodeQuery, RouteTranslationReadModel
    ]
):
    def __init__(
        self,
        route_reader: IRouteReader,
        route_translation_reader: IRouteTranslationReader,
    ) -> None:
        self._route_reader = route_reader
        self._route_translation_reader = route_translation_reader

    async def handle(
        self, query: GetAdminRouteTranslationByLanguageCodeQuery
    ) -> RouteTranslationReadModel:
        exists = await self._route_reader.exists(
            route_id=query.route_id,
        )
        if not exists:
            raise RouteNotFound(route_id=query.route_id)

        translation = (
            await self._route_translation_reader.get_by_route_id_and_language_code(
                route_id=query.route_id,
                language_code=query.language_code,
            )
        )
        if translation is None:
            raise RouteTranslationNotFound(
                route_id=query.route_id, language_code=query.language_code
            )

        return translation
