from pydantic import BaseModel


class SignInSchema(BaseModel):
    username: str
    password: str


class LogOutSchema(BaseModel):
    token: str
