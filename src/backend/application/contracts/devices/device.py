from pydantic import BaseModel

from backend.domain.entities.device import DeviceEntity
from backend.domain.enum.device import Platform


class DeviceResponse(BaseModel):
    id: int
    user_id: int
    platform: Platform

    @classmethod
    def from_entity(cls, entity: DeviceEntity) -> "DeviceResponse":
        return DeviceResponse(
            id=entity.id,
            user_id=entity.user_id,
            platform=entity.platform,
        )
