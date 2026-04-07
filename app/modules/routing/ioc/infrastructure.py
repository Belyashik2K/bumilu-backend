from dishka import (
    Provider,
    Scope,
    provide,
)

from app.core.infrastructure.config import AppConfig
from app.modules.routing.application.interfaces.routing_gateway import IRoutingGateway
from app.modules.routing.infrastructure.valhalla.client import ValhallaClient
from app.modules.routing.infrastructure.valhalla.routing_gateway import (
    ValhallaRoutingGateway,
)


class RoutingInfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    async def valhalla_client(self, config: AppConfig) -> ValhallaClient:
        return ValhallaClient(
            base_url=config.routing.valhalla.base_url,
            timeout=config.routing.valhalla.timeout_sec,
        )

    @provide(scope=Scope.APP, provides=IRoutingGateway)
    async def routing_gateway(
        self, valhalla_client: ValhallaClient
    ) -> ValhallaRoutingGateway:
        return ValhallaRoutingGateway(client=valhalla_client)
