from aiogram import Router

from .common import router as common_router
from .activity import router as activity_router
from .logging import router as logging_router


def get_routers() -> list[Router]:
    
    return [
        common_router,
        activity_router,
        logging_router,
    ]
