from aiogram import Router

from .common import router as common_router
from .logging import router as logging_router


def get_routers() -> list[Router]:
  
    return [
        logging_router,
        common_router,
    ]
