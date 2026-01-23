from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float, nullable=False, default=0)

    sender = relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_transactions",
    )

    receiver = relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="received_transactions",
    )