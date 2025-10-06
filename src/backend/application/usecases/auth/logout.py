from dataclasses import dataclass

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.contracts.auth.logout import LogOutRequest, LogOutResponse
from backend.infrastructure.cache.session import SessionGateway


@dataclass
class LogOutUseCase(Interactor[LogOutRequest, LogOutResponse]):
    id_provider: IdProvider

    session: SessionGateway

    async def __call__(self, _: LogOutRequest) -> LogOutResponse:
        # NOTE: just authenticate
        await self.id_provider.get_user()

        session_id = await self.id_provider.get_session_id()
        await self.session.logout(session_id)

        return LogOutResponse(success=True)
