from sqlalchemy import Column, Integer, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base


class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer(), primary_key=True, index=True, nullable=False)
    created_at = Column(DateTime(), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime())
    trader_id = Column(Integer(), ForeignKey('users.id'), nullable=False)
    purchaser_id = Column(Integer(), ForeignKey('users.id'))
    trading_rank_id = Column(Integer(), ForeignKey('ranks.id'))
    trading_amount = Column(Float())
    purchasing_rank_id = Column(Integer(), ForeignKey('ranks.id'))
    purchasing_amount = Column(Float())
    completed = Column(Boolean(), nullable=False, default=False)

    trader = relationship('User', foreign_keys=[trader_id], back_populates='trading_trades')
    purchaser = relationship('User', foreign_keys=[purchaser_id], back_populates='purchasing_trades')
    trading_rank = relationship('Rank', foreign_keys=[trading_rank_id], back_populates='trading_trades')
    purchasing_rank = relationship('Rank', foreign_keys=[purchasing_rank_id], back_populates='purchasing_trades')
