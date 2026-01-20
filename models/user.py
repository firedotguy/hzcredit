from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    name = Column(String, nullable=False)
    balance = Column(Float, nullable=False, default=0.0)

    # @property
    # def transactions(self):
    #     return sorted((self.sent_transactions or []) + (self.received_transactions or []), key=lambda t: t.created_at)