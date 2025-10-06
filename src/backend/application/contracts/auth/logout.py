from pydantic import BaseModel


class LogOutResponse(BaseModel):
    success: bool
