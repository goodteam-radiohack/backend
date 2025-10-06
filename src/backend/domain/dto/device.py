from pydantic import BaseModel

from backend.domain.enum.device import Platform


class CreateDeviceDTO(BaseModel):
    user_id: int
    token: str
    platform: Platform
