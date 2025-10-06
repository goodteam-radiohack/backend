from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

import jwt
from pytz import timezone

from backend.application.common.token_processor import TokenProcessor
from backend.infrastructure.errors.auth import UnauthenticatedError
from backend.infrastructure.settings import WebSettings

ALGORITHM = "HS256"


@dataclass
class JWTProcessor(TokenProcessor):
    web_settings: WebSettings

    def create_token(self, session_uuid: UUID) -> str:
        expires = datetime.now(tz=timezone("UTC")) + self.web_settings.jwt_expires_in
        payload = {"sub": str(session_uuid), "exp": expires}

        return jwt.encode(
            payload, self.web_settings.jwt_secret.get_secret_value(), ALGORITHM
        )

    def validate_token(self, token: str) -> UUID:
        try:
            payload = jwt.decode(
                token, self.web_settings.jwt_secret.get_secret_value(), [ALGORITHM]
            )
        except jwt.InvalidTokenError as exc:
            raise UnauthenticatedError from exc

        return UUID(payload["sub"])
