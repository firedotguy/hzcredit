from aiogram import Router

from . import back, rank, start, trade, transaction, top

base_router = Router()
base_router.include_routers(
    back.router,
    rank.router,
    start.router,
    trade.router,
    transaction.router,
    top.router
)