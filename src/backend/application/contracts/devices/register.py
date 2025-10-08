from pydantic import BaseModel

from backend.domain.enum.device import Platform


class RegisterDeviceRequest(BaseModel):
    token: str
    platform: Platform
