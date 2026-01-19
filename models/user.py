from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float

from db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    balance = Column(Float, nullable=False, default=0)