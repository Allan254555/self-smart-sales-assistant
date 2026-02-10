from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .connection import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    
    messages = relationship("Message", back_populates="user")
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True,index=True)
    user_id  = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    message = Column(Text, nullable=False)
    sender = Column(String(20),nullable=False)
    timestamp = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="messages")