from dataclasses import dataclass

from sqlalchemy import insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.gateways.user import UserReader, UserUpdater, UserWriter
from backend.domain.dto.user import CreateUserDTO
from backend.domain.entities.user import UserEntity
from backend.domain.enum.user import UserRole
from backend.infrastructure.database.models.user import UserModel
from backend.infrastructure.errors.gateways.user import UserNotFoundError


@dataclass
class UserGateway(UserReader, UserWriter, UserUpdater):
    session: AsyncSession

    async def with_id(self, user_id: int) -> UserEntity:
        stmt = select(UserModel).where(UserModel.id == user_id)

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise UserNotFoundError from exc

        return result.to_entity()

    async def with_username(self, username: str) -> UserEntity:
        stmt = select(UserModel).where(UserModel.username == username)

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise UserNotFoundError from exc

        return result.to_entity()

    async def create(self, dto: CreateUserDTO) -> UserEntity:
        stmt = (
            insert(UserModel)
            .values(
                username=dto.username,
                password=dto.hashed_password,
                role=dto.role,
            )
            .returning(UserModel.id)
        )

        user_id = (await self.session.execute(stmt)).scalar_one()

        return await self.with_id(user_id)

    async def update_role(self, user_id: int, role: UserRole) -> UserEntity:
        stmt = update(UserModel).values(role=role).where(UserModel.id == user_id)

        await self.session.execute(stmt)

        return await self.with_id(user_id)
