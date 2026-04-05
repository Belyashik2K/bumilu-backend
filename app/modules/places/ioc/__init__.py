from .commands import PlacesCommandHandlersProvider
from .infrastructure import PlacesInfrastructureProvider
from .persistence import PlacesPersistenceProvider
from .queries import PlacesQueryHandlersProvider

PLACES_PROVIDERS = [
    PlacesInfrastructureProvider(),
    PlacesPersistenceProvider(),
    PlacesCommandHandlersProvider(),
    PlacesQueryHandlersProvider(),
]
