from pydantic import BaseModel


class SignInRequest(BaseModel):
    username: str
    password: str


class SignInResponse(BaseModel):
    success: bool
    token: str
