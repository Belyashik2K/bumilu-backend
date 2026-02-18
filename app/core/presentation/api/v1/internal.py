from fastapi import APIRouter

internal_router = APIRouter(
    prefix="/internal",
    tags=["Internal"],
)
