from dishka import AnyOf, Provider, Scope, provide

from backend.application.gateways.device import DeviceReader, DeviceWriter
from backend.application.gateways.event import EventReader, EventUpdater, EventWriter
from backend.application.gateways.rsvp import RsvpReader, RsvpWriter
from backend.application.gateways.user import UserReader, UserUpdater, UserWriter
from backend.infrastructure.cache.session import SessionGateway
from backend.infrastructure.database.gateways.device import DeviceGateway
from backend.infrastructure.database.gateways.event import EventGateway
from backend.infrastructure.database.gateways.rsvp import RsvpGateway
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

    event_gateway = provide(
        EventGateway,
        provides=AnyOf[
            EventReader,
            EventWriter,
            EventUpdater,
        ],
    )

    rsvp_gateway = provide(
        RsvpGateway,
        provides=AnyOf[
            RsvpReader,
            RsvpWriter,
        ],
    )

    session_gateway = provide(SessionGateway)
