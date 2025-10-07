from pydantic import BaseModel

from backend.application.contracts.users.user import UserResponse


class GetUsersRequest(BaseModel):
    limit: int = 100
    offset: int = 0


class GetUsersResponse(BaseModel):
    items: list[UserResponse]
    total: int
