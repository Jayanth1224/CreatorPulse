from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class VoiceSampleBase(BaseModel):
    """Base model for voice training samples"""
    title: str = Field(..., min_length=1, max_length=200, description="Title for the writing sample")
    content: str = Field(..., min_length=50, max_length=10000, description="The writing content for voice training")


class VoiceSampleCreate(VoiceSampleBase):
    """Model for creating a new voice sample"""
    pass


class VoiceSampleUpdate(BaseModel):
    """Model for updating a voice sample"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=50, max_length=10000)


class VoiceSampleResponse(VoiceSampleBase):
    """Model for voice sample responses"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VoiceSamplesUploadRequest(BaseModel):
    """Model for bulk upload of voice samples"""
    samples: List[VoiceSampleCreate] = Field(..., min_items=1, max_items=50, description="List of writing samples")


class VoiceSamplesUploadResponse(BaseModel):
    """Response for bulk upload"""
    created_count: int
    sample_ids: List[str]
    message: str


class VoiceTrainingStatus(BaseModel):
    """Model for voice training status"""
    has_samples: bool
    sample_count: int
    last_updated: Optional[datetime] = None
    is_active: bool = Field(default=True, description="Whether voice training is currently active")
