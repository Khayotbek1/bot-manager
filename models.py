from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String)
    phone = Column(String, nullable=True)
    region = Column(String, nullable=True)

    joined_at = Column(DateTime, default=datetime.utcnow)
    left_at = Column(DateTime, nullable=True)

    is_registered = Column(Boolean, default=False)
