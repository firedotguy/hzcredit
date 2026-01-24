from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base


class Rank(Base):
    __tablename__ = 'ranks'

    id = Column(Integer(), primary_key=True, index=True, nullable=False)
    created_at = Column(DateTime(), nullable=False, server_default=func.now())
    owned_at = Column(DateTime())
    name = Column(String(), nullable=False, unique=True)
    owner_id = Column(Integer(), ForeignKey('users.id'))

    owner = relationship("User", foreign_keys=[owner_id], back_populates='ranks')
    trading_trades = relationship('Trade', foreign_keys='Trade.trading_rank_id', back_populates='trading_rank')
    purchasing_trades = relationship('Trade', foreign_keys='Trade.purchasing_rank_id', back_populates='purchasing_rank')