from dishka import make_async_container
from dishka.integrations.taskiq import setup_dishka

from app.core.di import ConfigProvider
from app.core.infrastructure.queue.broker import broker
from app.modules.auth.di import AuthEmailProvider

container = make_async_container(ConfigProvider(), AuthEmailProvider())
setup_dishka(broker=broker, container=container)

import app.modules.auth.infrastructure.queue.tasks
import app.modules.chat.infrastructure.queue.tasks  # noqa: F401
