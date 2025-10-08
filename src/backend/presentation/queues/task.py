from dishka import FromDishka
from dishka.integrations.taskiq import inject

from backend.application.contracts.devices.send_notification import (
    SendNotificationRequest,
)
from backend.application.usecases.devices.send_notifications import (
    SendNotificationsUseCase,
)

from . import broker


@broker.task(schedule=[{"cron": "* * * * *"}])
@inject(patch_module=True)
async def send_notifications(interactor: FromDishka[SendNotificationsUseCase]) -> None:
    await interactor(SendNotificationRequest())
