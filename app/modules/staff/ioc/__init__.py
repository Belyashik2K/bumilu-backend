from app.modules.staff.ioc.commands import StaffCommandHandlersProvider
from app.modules.staff.ioc.persistence import StaffPersistenceProvider
from app.modules.staff.ioc.queries import StaffQueryHandlersProvider

STAFF_PROVIDERS = [
    StaffPersistenceProvider(),
    StaffCommandHandlersProvider(),
    StaffQueryHandlersProvider(),
]
