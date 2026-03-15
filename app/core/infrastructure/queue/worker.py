from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka

import app.core.infrastructure.database.models_registry
from app.core.di import (
    ConfigProvider,
    DatabaseProvider,
)
from app.core.infrastructure.queue.broker import broker
from app.modules.auth.di import AuthEmailProvider
from app.modules.chat.di import (
    CHAT_PROVIDERS,
)
from app.modules.users.di import UserProvider

container = make_async_container(
    ConfigProvider(),
    DatabaseProvider(),
    AuthEmailProvider(),
    UserProvider(),
    *CHAT_PROVIDERS,
)
setup_dishka(broker=broker, container=container)

import app.modules.auth.infrastructure.queue.tasks
import app.modules.chat.infrastructure.queue.tasks  # noqa: F401
