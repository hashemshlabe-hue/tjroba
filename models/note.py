from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

class NoteCategory(str, enum.Enum):
    FIQH = "fiqh"
    LUGHA = "lugha"
    USOOL = "usool"
    HADITH = "hadith"
    SEERAH = "seerah"
    GENERAL = "general"

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(Enum(NoteCategory), default=NoteCategory.GENERAL, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", backref="notes")

    def __repr__(self):
        return f"<Note(id={self.id}, category={self.category.value})>"
