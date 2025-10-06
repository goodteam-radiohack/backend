from pydantic import BaseModel

from backend.domain.enum.user import UserRole


class CreateUserDTO(BaseModel):
    username: str
    hashed_password: str

    role: UserRole = UserRole.DEPUTE
