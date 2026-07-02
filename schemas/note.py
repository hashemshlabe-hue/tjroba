from pydantic import BaseModel, Field
from datetime import datetime
from models.note import NoteCategory
from typing import Optional

class NoteCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    category: NoteCategory = Field(default=NoteCategory.GENERAL)

class NoteUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=2000)
    category: Optional[NoteCategory] = None

class NoteResponse(BaseModel):
    id: int
    user_id: int
    content: str
    category: NoteCategory
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
