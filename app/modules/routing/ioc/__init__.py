from .infrastructure import RoutingInfrastructureProvider
from .queries import RoutingQueryHandlersProvider

ROUTING_PROVIDERS = [
    RoutingInfrastructureProvider(),
    RoutingQueryHandlersProvider(),
]
