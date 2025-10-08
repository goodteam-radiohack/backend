from dataclasses import dataclass

from sqlalchemy import delete, insert, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.gateways.device import DeviceReader, DeviceWriter
from backend.domain.dto.device import CreateDeviceDTO
from backend.domain.entities.device import DeviceEntity
from backend.infrastructure.database.models.devices import DeviceModel
from backend.infrastructure.errors.gateways.device import DeviceNotFoundError


@dataclass
class DeviceGateway(DeviceReader, DeviceWriter):
    session: AsyncSession

    async def with_id(self, device_id: int) -> DeviceEntity:
        stmt = select(DeviceModel).where(DeviceModel.id == device_id)

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise DeviceNotFoundError from exc

        return result.to_entity()

    async def with_user_id(self, user_id: int) -> list[DeviceEntity]:
        stmt = select(DeviceModel).where(DeviceModel.user_id == user_id)

        results = (await self.session.scalars(stmt)).all()

        return [result.to_entity() for result in results]

    async def with_user_id_and_token(self, user_id: int, token: str) -> DeviceEntity:
        stmt = select(DeviceModel).where(
            DeviceModel.user_id == user_id, DeviceModel.token == token
        )

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise DeviceNotFoundError from exc

        return result.to_entity()

    async def create(self, dto: CreateDeviceDTO) -> DeviceEntity:
        stmt = (
            insert(DeviceModel)
            .values(user_id=dto.user_id, token=dto.token, platform=dto.platform)
            .returning(DeviceModel.id)
        )

        device_id = (await self.session.execute(stmt)).scalar_one()

        return await self.with_id(device_id)

    async def delete(self, device_id: int) -> None:
        stmt = delete(DeviceModel).where(DeviceModel.id == device_id)
        await self.session.execute(stmt)
