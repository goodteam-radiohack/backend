from dataclasses import dataclass

from backend.domain.entities.user import UserEntity


@dataclass
class GetMeRequest:
    pass


@dataclass
class GetMeResponse:
    user: UserEntity
