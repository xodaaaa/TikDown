from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, Response

from src.config import settings
from src.core.auth import is_setup_complete, setup_admin_password, verify_admin_password
from src.schemas.auth import AuthResponse, LoginRequest, SetupRequest

router = APIRouter()

SESSION_COOKIE = "tikdown_session"
IS_SETUP_DONE = False


@router.post("/auth/setup", response_model=AuthResponse)
async def setup(request: Request, data: SetupRequest):
    global IS_SETUP_DONE
    if IS_SETUP_DONE or is_setup_complete():
        raise HTTPException(status_code=400, detail="Setup already completed")

    hash_val = setup_admin_password(data.password)
    settings.ADMIN_PASSWORD_HASH = hash_val
    IS_SETUP_DONE = True

    response = AuthResponse(authenticated=True, message="Admin password set successfully")
    resp = Response(
        content=response.model_dump_json(),
        media_type="application/json",
    )
    session_data = "authenticated"
    resp.set_cookie(
        key=SESSION_COOKIE,
        value=session_data,
        httponly=True,
        samesite="lax",
        max_age=86400 * 30,
    )
    return resp


@router.post("/auth/login", response_model=AuthResponse)
async def login(data: LoginRequest):
    if not is_setup_complete():
        raise HTTPException(status_code=400, detail="Setup not completed. Call /api/auth/setup first")

    if not verify_admin_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    response = AuthResponse(authenticated=True, message="Login successful")
    resp = Response(
        content=response.model_dump_json(),
        media_type="application/json",
    )
    resp.set_cookie(
        key=SESSION_COOKIE,
        value="authenticated",
        httponly=True,
        samesite="lax",
        max_age=86400 * 30,
    )
    return resp


@router.post("/auth/logout")
async def logout():
    resp = Response(content='{"message":"Logged out"}', media_type="application/json")
    resp.delete_cookie(SESSION_COOKIE)
    return resp


@router.get("/auth/check", response_model=AuthResponse)
async def check_auth(request: Request):
    session = request.cookies.get(SESSION_COOKIE)
    if session == "authenticated":
        return AuthResponse(authenticated=True)
    return AuthResponse(authenticated=False, message="Not authenticated")


async def require_auth(request: Request):
    if not is_setup_complete():
        return
    session = request.cookies.get(SESSION_COOKIE)
    if session != "authenticated":
        raise HTTPException(status_code=401, detail="Authentication required")
