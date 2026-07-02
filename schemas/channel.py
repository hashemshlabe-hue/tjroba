from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from models.channel import ChannelType
from typing import Optional

class ChannelCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    link: str = Field(..., min_length=1, max_length=500)
    type: ChannelType
    description: Optional[str] = Field(None, max_length=500)

class ChannelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    link: Optional[str] = Field(None, min_length=1, max_length=500)
    type: Optional[ChannelType] = None
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class ChannelResponse(BaseModel):
    id: int
    name: str
    link: str
    type: ChannelType
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
