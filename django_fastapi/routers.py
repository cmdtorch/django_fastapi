from fastapi import APIRouter


api_router = APIRouter()

api_router.include_router(api_router, prefix='/auth', tags=["auth"])
