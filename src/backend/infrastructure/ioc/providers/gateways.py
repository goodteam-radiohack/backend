from dishka import AnyOf, Provider, Scope, provide

from backend.application.gateways.device import DeviceReader, DeviceWriter
from backend.application.gateways.user import UserReader, UserUpdater, UserWriter
from backend.infrastructure.database.gateways.device import DeviceGateway
from backend.infrastructure.database.gateways.user import UserGateway


class GatewaysProvider(Provider):
    scope = Scope.REQUEST

    user_gateway = provide(
        UserGateway,
        provides=AnyOf[
            UserReader,
            UserWriter,
            UserUpdater,
        ],
    )

    device_gateway = provide(
        DeviceGateway,
        provides=AnyOf[
            DeviceReader,
            DeviceWriter,
        ],
    )
