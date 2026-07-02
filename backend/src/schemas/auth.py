from pydantic import BaseModel


class LoginRequest(BaseModel):
    password: str


class AuthResponse(BaseModel):
    authenticated: bool
    needs_setup: bool = False
    message: str = ""


class SetupRequest(BaseModel):
    password: str
