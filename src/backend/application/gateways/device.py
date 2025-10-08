from typing import Protocol

from backend.domain.dto.device import CreateDeviceDTO
from backend.domain.entities.device import DeviceEntity


class DeviceReader(Protocol):
    async def with_id(self, device_id: int) -> DeviceEntity: ...
    async def with_user_id(self, user_id: int) -> list[DeviceEntity]: ...
    async def with_user_id_and_token(
        self, user_id: int, token: str
    ) -> DeviceEntity: ...


class DeviceWriter(Protocol):
    async def create(self, dto: CreateDeviceDTO) -> DeviceEntity: ...
    async def delete(self, device_id: int) -> None: ...
