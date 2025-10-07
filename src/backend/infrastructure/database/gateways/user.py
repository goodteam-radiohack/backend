from dataclasses import dataclass

from sqlalchemy import func, insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.application.gateways.user import UserReader, UserUpdater, UserWriter
from backend.domain.dto.user import CreateUserDTO
from backend.domain.entities.user import UserEntity
from backend.domain.enum.user import UserRole
from backend.infrastructure.database.models.user import UserModel
from backend.infrastructure.errors.gateways.user import UserNotFoundError

_OPTIONS = [joinedload(UserModel.helping_to), joinedload(UserModel.helper)]


@dataclass
class UserGateway(UserReader, UserWriter, UserUpdater):
    session: AsyncSession

    async def with_id(self, user_id: int) -> UserEntity:
        stmt = select(UserModel).where(UserModel.id == user_id).options(*_OPTIONS)

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise UserNotFoundError from exc

        return result.to_entity()

    async def with_username(self, username: str) -> UserEntity:
        stmt = (
            select(UserModel).where(UserModel.username == username).options(*_OPTIONS)
        )

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise UserNotFoundError from exc

        return result.to_entity()

    async def all(self, limit: int, offset: int) -> tuple[list[UserEntity], int]:
        stmt = (
            select(UserModel)
            .limit(limit)
            .offset(offset)
            .order_by(UserModel.id)
            .options(*_OPTIONS)
        )
        total_stmt = select(func.count(UserModel.id)).select_from(UserModel)

        results = (await self.session.scalars(stmt)).all()
        total_result = (await self.session.scalars(total_stmt)).one()

        return [result.to_entity() for result in results], total_result

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
