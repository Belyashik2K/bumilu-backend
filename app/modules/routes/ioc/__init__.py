from .infrastructure import RoutesInfrastructureProvider
from .queries import RoutesQueryHandlersProvider

ROUTES_PROVIDERS = [
    RoutesInfrastructureProvider(),
    RoutesQueryHandlersProvider(),
]
