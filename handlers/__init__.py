from aiogram import Router

from . import history, rank, start, trade, transaction

base_router = Router()
base_router.include_routers(
    history.router,
    rank.router,
    start.router,
    trade.router,
    transaction.router
)