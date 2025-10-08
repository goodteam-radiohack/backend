from dishka.integrations.taskiq import setup_dishka
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NatsBroker

from backend.infrastructure.ioc import get_container
from backend.infrastructure.settings import get_settings

settings = get_settings()
broker = NatsBroker(servers=settings.nats.build_connection_uri())

container = get_container()
setup_dishka(container, broker)

scheduler = TaskiqScheduler(
    broker,
    sources=[LabelScheduleSource(broker)],
)

__all__ = ("broker",)
