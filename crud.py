from datetime import datetime
from typing import cast

from sqlalchemy.orm import Session

from models import *
from logger import get_logger

l = get_logger()


def get_user(db: Session, user_id: int) -> User | None:
    l.info('get user user_id=%s', user_id)
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        l.info('found user id=%s', user.id)
    else:
        l.error('user not found')
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
    l.info('user created id=%s', user.id)
    return user

def get_user_top(db: Session) -> list[User]:
    l.info('get user top')
    users = db.query(User).order_by(User.balance.desc()).limit(10).all()
    l.info('fetched users top ids=%s', [user.id for user in users])
    return users


def get_rank(db: Session, id: int) -> Rank | None:
    l.info('get rank id=%s', id)
    rank = db.query(Rank).filter(Rank.id == id).first()
    if rank:
        l.info('found rank name=%s', rank.name)
    else:
        l.error('rank not found')
    return rank

def get_rank_by_name(db: Session, name: str) -> Rank | None:
    l.info('get rank name=%s', name)
    rank = db.query(Rank).filter(Rank.name == name).first()
    if rank:
        l.info('found rank id=%s', rank.id)
    else:
        l.error('rank not found')
    return rank

def transfer_rank(db: Session, rank: Rank, receiver_id: int) -> Rank:
    l.info('transfer rank id=%s receiver_id=%s', rank.id, receiver_id)
    db.query(Rank).where(Rank.id == rank.id).update({'owner_id': receiver_id, 'owned_at': datetime.now().replace(microsecond=0)})
    db.refresh(rank)
    l.info('rank transfered')
    return rank


def get_trades(db: Session, only_open: bool = True, trader_id: int | None = None, purchaser_id: int | None = None) -> list[Trade]:
    l.info('get trades only_open=%s trader_id=%s purchaser_id=%s', only_open, trader_id, purchaser_id)
    query = db.query(Trade)
    if trader_id:
        query = query.where(Trade.trader_id == trader_id)
    if purchaser_id:
        query = query.where(Trade.purchaser_id == purchaser_id)
    if only_open:
        query = query.where(Trade.completed != True).where(Trade.deleted != True)
    trades = query.order_by(Trade.created_at.desc()).limit(50).all()
    l.info('fetched trades ids=%s', [trade.id for trade in trades])
    return trades


def get_trade(db: Session, id: int) -> Trade | None:
    l.info('get trade id=%s', id)
    trade = db.query(Trade).where(Trade.id == id).first()
    if trade:
        l.info('found trade')
    else:
        l.error('trade not found')
    return trade

def create_trade(db: Session, trade: Trade) -> Trade:
    l.info('create trade')
    db.add(trade)
    db.commit()
    db.refresh(trade)
    l.info('trade created id=%s', trade.id)
    return trade

def delete_trade(db: Session, id: int):
    l.info('delete trade id=%s', id)
    db.query(Trade).where(Trade.id == id).update({'deleted': True})
    db.commit()
    l.info('trade deleted')

def accept_trade(db: Session, id: int, user_id: int) -> None:
    l.info('accept trade id=%s user_id=%s', id, user_id)
    db.query(Trade).where(Trade.id == id).update({'purchaser_id': user_id, 'completed': True})
    db.commit()
    l.info('trade accepted')


def make_transaction(db: Session, amount: float, sender: User, receiver: User) -> Transaction | None:
    l.info('make transaction amount=%s sender_id=%s receiver_id=%s', amount, sender.id, receiver.id)
    if cast(float, sender.balance) - amount < 0:
        l.error('sender balance insufficient')
        return

    transaction = Transaction(
        sender_id=sender.id,
        receiver_id=receiver.id,
        amount=amount
    )
    db.add(transaction)
    db.query(User).where(User.id == sender.id).update({'balance': sender.balance - amount})
    db.query(User).where(User.id == receiver.id).update({'balance': receiver.balance + amount})
    db.commit()
    db.refresh(transaction)

    return transaction
