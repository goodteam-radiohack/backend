from backend.domain.entities.base import BaseEntity
from backend.domain.enum.device import Platform


class DeviceEntity(BaseEntity):
    id: int

    user_id: int

    token: str
    platform: Platform
