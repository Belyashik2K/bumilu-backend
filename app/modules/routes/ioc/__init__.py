from .commands import RoutesCommandHandlersProvider
from .persistence import RoutesPersistenceProvider
from .queries import RoutesQueryHandlersProvider

ROUTES_PROVIDERS = [
    RoutesPersistenceProvider(),
    RoutesCommandHandlersProvider(),
    RoutesQueryHandlersProvider(),
]
