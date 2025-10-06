from pydantic import BaseModel


class SignInResponse(BaseModel):
    success: bool
    token: str
