from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True, index=True, nullable=False)
    user_id = Column(Integer(), nullable=False, unique=True)
    created_at = Column(DateTime(), nullable=False, server_default=func.now())
    name = Column(String(), nullable=False)
    balance = Column(Float(), nullable=False, default=0.0)

    ranks = relationship('Rank', foreign_keys="Rank.owner_id", back_populates='owner')

    sent_transactions = relationship("Transaction", foreign_keys="Transaction.sender_id", back_populates="sender")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.receiver_id", back_populates="receiver")
    trading_trades = relationship('Trade', foreign_keys='Trade.trader_id', back_populates='trader')
    purchasing_trades = relationship('Trade', foreign_keys='Trade.purchaser_id', back_populates='purchaser')

    @property
    def transactions(self):
        return sorted((self.sent_transactions or []) + (self.received_transactions or []), key=lambda t: t.created_at)