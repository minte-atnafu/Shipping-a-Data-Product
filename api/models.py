from sqlalchemy import Column, Integer, String, Date, Float, Boolean
from .database import Base

class Message(Base):
    __tablename__ = "fct_messages"
    __table_args__ = {'schema': 'public'}  # Temporarily point to public schema
    message_id = Column(String, primary_key=True)
    channel_id = Column(Integer)
    message_date = Column(Date)
    message_text = Column(String)
    has_image = Column(Boolean)
    message_length = Column(Integer)
    has_text = Column(Boolean)
    product_name = Column(String)

class Channel(Base):
    __tablename__ = "dim_channels"
    __table_args__ = {'schema': 'marts'}  # Assuming dim_channels is in marts
    channel_id = Column(Integer, primary_key=True)
    channel_name = Column(String)

class ImageDetection(Base):
    __tablename__ = "image_detections"
    __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True)
    message_id = Column(String)
    detected_object_class = Column(String)
    confidence_score = Column(Float)