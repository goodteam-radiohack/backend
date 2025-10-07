from typing import Self

from pydantic import BaseModel, model_validator

from backend.domain.enum.user import UserRole


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.DEPUTE
    helping_for_id: int | None = None

    @model_validator(mode="after")
    def _validate(self) -> Self:
        if self.role != UserRole.DEPUTE_HELPER and self.helping_for_id is not None:
            raise ValueError

        if self.role == UserRole.DEPUTE and self.helping_for_id is None:
            raise ValueError

        return self
