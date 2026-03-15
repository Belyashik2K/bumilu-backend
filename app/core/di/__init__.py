from .config import ConfigProvider
from .database import DatabaseProvider
from .redis import RedisProvider
from .scheduler import SchedulerProvider

CORE_PROVIDERS = [
    ConfigProvider(),
    DatabaseProvider(),
    RedisProvider(),
    SchedulerProvider(),
]
