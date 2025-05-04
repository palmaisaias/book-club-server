from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)

class MonthlyPick(Base):
    __tablename__ = "monthly_picks"

    id = Column(Integer, primary_key=True, index=True)
    suggestion_id = Column(Integer, ForeignKey("suggestions.id"), nullable=False)
    month       = Column(String, unique=True, nullable=False)   # e.g. "2025-05"

    suggestion = relationship("Suggestion")

class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)