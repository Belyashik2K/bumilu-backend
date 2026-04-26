from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka

from app.core.infrastructure.queue.broker import broker
from app.core.ioc import (
    ConfigProvider,
    DatabaseProvider,
)
from app.modules.auth.ioc import AuthEmailProvider
from app.modules.chat.ioc import (
    CHAT_PROVIDERS,
)
from app.modules.places.ioc import PlacesPersistenceProvider
from app.modules.users.ioc import UserProvider

container = make_async_container(
    ConfigProvider(),
    DatabaseProvider(),
    AuthEmailProvider(),
    UserProvider(),
    PlacesPersistenceProvider(),
    *CHAT_PROVIDERS,
)
setup_dishka(broker=broker, container=container)

import app.modules.chat.infrastructure.queue.tasks  # noqa: F401
