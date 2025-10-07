from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.contracts.users.get import GetUsersRequest, GetUsersResponse
from backend.application.contracts.users.user import UserResponse
from backend.application.errors.access import UnauthorizedError
from backend.application.gateways.user import UserReader
from backend.domain.enum.user import UserRole


@dataclass
class GetUsersUseCase(Interactor[GetUsersRequest, GetUsersResponse]):
    id_provider: IdProvider

    user_reader: UserReader

    async def __call__(self, data: GetUsersRequest) -> GetUsersResponse:
        user = await self.id_provider.get_user()

        if user.role != UserRole.ADMIN:
            raise UnauthorizedError

        users, total = await self.user_reader.all(data.limit, data.offset)

        return GetUsersResponse(
            items=[UserResponse.from_entity(user) for user in users],
            total=total,
        )
