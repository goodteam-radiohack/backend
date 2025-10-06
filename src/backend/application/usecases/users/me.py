from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.contracts.users.me import GetMeRequest, GetMeResponse
from backend.application.contracts.users.user import UserResponse


@dataclass
class GetMeUseCase(Interactor[GetMeRequest, GetMeResponse]):
    id_provider: IdProvider

    async def __call__(self, _: GetMeRequest) -> GetMeResponse:
        user = await self.id_provider.get_user()

        return GetMeResponse(
            user=UserResponse.from_entity(user),
        )
