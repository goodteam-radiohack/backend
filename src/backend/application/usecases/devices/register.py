from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.common.uow import UnitOfWork
from backend.application.contracts.devices.device import DeviceResponse
from backend.application.contracts.devices.register import RegisterDeviceRequest
from backend.application.gateways.device import DeviceReader, DeviceWriter
from backend.domain.dto.device import CreateDeviceDTO
from backend.infrastructure.errors.gateways.device import DeviceNotFoundError


@dataclass
class RegisterDeviceUseCase(Interactor[RegisterDeviceRequest, DeviceResponse]):
    id_provider: IdProvider

    device_reader: DeviceReader
    device_writer: DeviceWriter

    uow: UnitOfWork

    async def __call__(self, data: RegisterDeviceRequest) -> DeviceResponse:
        user = await self.id_provider.get_user()

        try:
            existing_device = await self.device_reader.with_user_id_and_token(
                user.id, data.token
            )
            return DeviceResponse.from_entity(existing_device)
        except DeviceNotFoundError:
            pass

        async with self.uow:
            device = await self.device_writer.create(
                CreateDeviceDTO(
                    user_id=user.id,
                    token=data.token,
                    platform=data.platform,
                )
            )

            await self.uow.commit()

        return DeviceResponse.from_entity(device)
