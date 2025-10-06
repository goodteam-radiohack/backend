from pydantic import BaseModel


class LogOutRequest(BaseModel):
    pass


class LogOutResponse(BaseModel):
    success: bool
