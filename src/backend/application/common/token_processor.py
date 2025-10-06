from typing import Protocol
from uuid import UUID


class TokenProcessor(Protocol):
    def create_token(self, session_uuid: UUID) -> str: ...
    def validate_token(self, token: str) -> UUID: ...
