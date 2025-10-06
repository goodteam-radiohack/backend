from dataclasses import dataclass

from backend.application.common.interactor import Interactor
from backend.application.contracts.users.me import MeRequest, MeResponse
from backend.application.common.id_provider import IdProvider

@dataclass
class MeUseCase(Interactor[MeRequest, MeResponse]):
    id_provider: IdProvider

    async def __call__(self, _: MeRequest) -> MeResponse:
        user = await self.id_provider.get_user()
        return MeResponse(user=user)
