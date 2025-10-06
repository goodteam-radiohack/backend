from dataclasses import dataclass

from backend.application.contracts.users.user import UserResponse


@dataclass
class GetMeRequest:
    pass


@dataclass
class GetMeResponse:
    user: UserResponse
