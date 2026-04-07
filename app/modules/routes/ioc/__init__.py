from .persistence import RoutesPersistenceProvider
from .queries import RoutesQueryHandlersProvider

ROUTES_PROVIDERS = [
    RoutesPersistenceProvider(),
    RoutesQueryHandlersProvider(),
]
