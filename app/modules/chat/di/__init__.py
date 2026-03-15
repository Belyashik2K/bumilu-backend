from .commands import ChatCommandHandlersProvider
from .infrastructure import ChatInfrastructureProvider
from .persistence import ChatPersistenceProvider
from .queries import ChatQueryHandlersProvider

CHAT_PROVIDERS = [
    ChatInfrastructureProvider(),
    ChatPersistenceProvider(),
    ChatQueryHandlersProvider(),
    ChatCommandHandlersProvider(),
]
