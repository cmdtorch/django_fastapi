from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from django.conf import settings

from core.middleware import middleware
from .asgi import application
from .routers import api_router

fastapp = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version=settings.VERSION,
    middleware=middleware
)


fastapp.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapp.include_router(api_router, prefix=settings.API_PREFIX)


if settings.MOUNT_DJANGO_APP:
    fastapp.mount("/django", application)
    fastapp.mount("/static", StaticFiles(directory=settings.STATIC_ROOT), name="static")
    fastapp.mount("/media", StaticFiles(directory=settings.MEDIA_SRC), name="static")
