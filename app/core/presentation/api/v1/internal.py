from fastapi import APIRouter

router = APIRouter(
    prefix="/internal",
    tags=["Internal"],
)
