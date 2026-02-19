from fastapi import APIRouter

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post("/login/guest")
async def login_as_guest() -> None:
    raise NotImplementedError


@auth_router.post("/login/email/request")
async def request_email_code() -> None:
    raise NotImplementedError


@auth_router.post("/login/email/verify")
async def verify_email_login() -> None:
    raise NotImplementedError


@auth_router.post("/refresh")
async def refresh() -> None:
    raise NotImplementedError


@auth_router.post("/logout")
async def logout() -> None:
    raise NotImplementedError
