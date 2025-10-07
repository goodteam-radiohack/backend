from dataclasses import dataclass

import aiobcrypt

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.common.uow import UnitOfWork
from backend.application.contracts.users.create import CreateUserRequest
from backend.application.contracts.users.user import UserResponse
from backend.application.errors.access import UnauthorizedError
from backend.application.gateways.user import UserWriter
from backend.domain.dto.user import CreateUserDTO
from backend.domain.enum.user import UserRole


@dataclass
class CreateUserUseCase(Interactor[CreateUserRequest, UserResponse]):
    id_provider: IdProvider

    user_writer: UserWriter
    uow: UnitOfWork

    async def __call__(self, data: CreateUserRequest) -> UserResponse:
        user = await self.id_provider.get_user()

        if user.role != UserRole.ADMIN:
            raise UnauthorizedError

        hashed_password = await aiobcrypt.hashpw_with_salt(data.password.encode())

        async with self.uow:
            user = await self.user_writer.create(
                CreateUserDTO(
                    username=data.username,
                    hashed_password=hashed_password.decode(),
                    role=data.role,
                    helping_for_id=data.helping_for_id,
                )
            )

            await self.uow.commit()

        return UserResponse.from_entity(user)
