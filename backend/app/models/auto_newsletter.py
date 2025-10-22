from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .base import Base

class AutoNewsletter(Base):
    __tablename__ = "auto_newsletters"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    bundle_id = Column(UUID(as_uuid=True), nullable=False)
    is_active = Column(Boolean, default=True)
    schedule_time = Column(String, default="08:00:00")  # Time in HH:MM:SS format
    schedule_frequency = Column(String, default="daily")  # daily, weekly, monthly
    schedule_day = Column(Integer)  # For weekly (1-7) or monthly (1-31)
    email_recipients = Column(ARRAY(Text))  # Array of email addresses
    last_generated = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "bundle_id": str(self.bundle_id),
            "is_active": self.is_active,
            "schedule_time": self.schedule_time,
            "schedule_frequency": self.schedule_frequency,
            "schedule_day": self.schedule_day,
            "email_recipients": self.email_recipients or [],
            "last_generated": self.last_generated.isoformat() if self.last_generated else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
