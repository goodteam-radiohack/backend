from dataclasses import dataclass
from uuid import UUID

from fastapi import Request

from backend.application.common.id_provider import IdProvider
from backend.application.common.token_processor import TokenProcessor
from backend.application.gateways.user import UserReader
from backend.domain.entities.user import UserEntity
from backend.infrastructure.cache.session import SessionGateway
from backend.infrastructure.errors.auth import UnauthenticatedError


@dataclass
class UserIdProvider(IdProvider):
    request: Request

    user_reader: UserReader
    session: SessionGateway

    token_processor: TokenProcessor

    def extract_token(self) -> str:
        authorization = self.request.headers.get("authorization")

        if authorization is None:
            raise UnauthenticatedError

        try:
            _, token = authorization.split("Bearer ")
        except ValueError as exc:
            raise UnauthenticatedError from exc

        return token

    async def get_session_id(self) -> UUID:
        token = self.extract_token()

        return self.token_processor.validate_token(token)

    async def get_user(self) -> UserEntity:
        session_id = await self.get_session_id()
        user_id = await self.session.with_id(session_id)

        return await self.user_reader.with_id(user_id)
