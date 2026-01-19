from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class ProductResponse(BaseModel):
    message_text: Optional[str]
    views: int

class ChannelActivity(BaseModel):
    message_date: date
    post_count: int

class VisualStat(BaseModel):
    image_category: str
    count: int

class MessageSearchResponse(BaseModel):
    message_text: Optional[str]
    views: int