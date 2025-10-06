from dataclasses import dataclass
from backend.domain.entities.user import UserEntity

@dataclass
class MeRequest:
    pass

@dataclass
class MeResponse:
    user: UserEntity
