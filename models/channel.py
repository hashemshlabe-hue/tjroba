from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from database import Base
import enum

class ChannelType(str, enum.Enum):
    COLLEGE = "college"
    DAWAH = "dawah"
    GROUP = "group"

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    type = Column(Enum(ChannelType), nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Channel(id={self.id}, name={self.name}, type={self.type.value})>"
