"""
FastAPI route configuration

Example:
Import your app route:
    from user.api import user_route

Then include them with params to main `api_router` below:
    api_router.include_router(user_route, prefix='/user', tags=["user"])
"""
from fastapi import APIRouter


api_router = APIRouter()


