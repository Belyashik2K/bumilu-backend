from .infrastructure import PlacesInfrastructureProvider
from .queries import PlacesQueryHandlersProvider

PLACES_PROVIDERS = [
    PlacesInfrastructureProvider(),
    PlacesQueryHandlersProvider(),
]
