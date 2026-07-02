from pydantic import BaseModel


class LoginRequest(BaseModel):
    password: str


class AuthResponse(BaseModel):
    authenticated: bool
    message: str = ""


class SetupRequest(BaseModel):
    password: str
