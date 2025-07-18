from pydantic import BaseModel
from datetime import date

class Message(BaseModel):
    message_id: str
    channel_id: int
    message_date: date
    message_text: str
    has_image: bool
    message_length: int
    has_text: bool
    product_name: str

    class Config:
        from_attributes = True  # Updated from orm_mode to from_attributes for Pydantic V2

class ProductReport(BaseModel):
    product_name: str
    mention_count: int

class ChannelActivity(BaseModel):
    message_date: date
    message_count: int