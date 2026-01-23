from sqlalchemy.orm import Session

from models import *
from logger import get_logger

l = get_logger()


def get_user(db: Session, user_id: int) -> User | None:
    l.info('get user user_id=%s', user_id)
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        l.info('found user id=%s', user.id)
    return user

def create_user(db: Session, name: str, user_id: int) -> User:
    l.info('create user user_id=%s name=%s', user_id, name)
    user = User(
        name=name,
        user_id=user_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    l.debug('user created id=%s', user.id)
    return user


def get_rank(db: Session, id: int) -> Rank:
    l.info('get rank id=%s', id)
    rank = db.query(Rank).filter(Rank.id == id).first()
    if rank:
        l.info('found rank name=%s', rank.name)
    return rank


def get_user_top(db: Session) -> list[User]:
    l.info('get user top')
    users = db.query(User).order_by(User.balance.desc()).limit(10).all()
    l.info('fetched users top ids=%s', [user.id for user in users])
    return users