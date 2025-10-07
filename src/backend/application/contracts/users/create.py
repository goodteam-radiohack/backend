from pydantic import BaseModel

from backend.domain.enum.user import UserRole


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.DEPUTE
