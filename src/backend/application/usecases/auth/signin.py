from dataclasses import dataclass

import aiobcrypt

from backend.application.common.interactor import Interactor
from backend.application.common.token_processor import TokenProcessor
from backend.application.contracts.auth.signin import SignInRequest, SignInResponse
from backend.application.errors.auth import CredentialsInvalidError
from backend.application.gateways.user import UserReader
from backend.infrastructure.cache.session import SessionGateway
from backend.infrastructure.errors.gateways.user import UserNotFoundError
from backend.infrastructure.settings import AppSettings


@dataclass
class SignInUseCase(Interactor[SignInRequest, SignInResponse]):
    user_reader: UserReader

    settings: AppSettings

    session: SessionGateway
    token_processor: TokenProcessor

    async def __call__(self, data: SignInRequest) -> SignInResponse:
        try:
            user = await self.user_reader.with_username(data.username)
        except UserNotFoundError as exc:
            raise CredentialsInvalidError from exc

        is_valid = await aiobcrypt.checkpw(
            data.password.encode(), user.password.encode()
        )
        if not is_valid:
            raise CredentialsInvalidError

        session_id = await self.session.create(
            user.id, self.settings.web.jwt_expires_in
        )
        token = self.token_processor.create_token(session_id)

        return SignInResponse(
            success=True,
            token=token,
        )
