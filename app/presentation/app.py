from fastapi import (
    FastAPI,
    APIRouter,
)

router = APIRouter(
    prefix="/api/v1",
    tags=["API"],
)


@router.get("/hello")
async def hello() -> dict:
    return {"message": "Hello, BumiLu!"}


app = FastAPI(
    title="BumiLu API",
    description="API for BumiLu application",
    version="1.0.0",
)
app.include_router(router)
