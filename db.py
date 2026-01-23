from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import TelegramObject
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from aiogram import BaseMiddleware

from logger import get_logger

l = get_logger()

engine = create_engine(
    "sqlite:///database.db",
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_db():
    l.debug('create db')
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    l.debug('get db')
    return SessionLocal()


class DBMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: dict[str, Any]) -> Any:
        l.debug('run db middleware')
        data['db'] = get_db()
        res = await handler(event, data)
        data['db'].close()
        return res