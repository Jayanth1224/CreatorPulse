from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Literal, Dict, Any


ToneType = Literal["professional", "conversational", "analytical", "friendly"]
DraftStatus = Literal["draft", "sent", "scheduled"]


class GenerateDraftRequest(BaseModel):
    bundle_id: str
    topic: Optional[str] = None
    tone: ToneType = "professional"


class DraftBase(BaseModel):
    bundle_id: str
    topic: Optional[str] = None
    tone: ToneType = "professional"


class DraftCreate(DraftBase):
    user_id: str
    bundle_name: str
    generated_html: str
    sources: List[str] = []


class DraftUpdate(BaseModel):
    edited_html: Optional[str] = None
    status: Optional[DraftStatus] = None
    scheduled_for: Optional[datetime] = None


class Draft(DraftBase):
    id: str
    user_id: str
    bundle_name: str
    generated_html: str
    edited_html: Optional[str] = None
    status: DraftStatus = "draft"
    readiness_score: Optional[int] = None
    sources: List[str] = []
    created_at: datetime
    updated_at: datetime
    sent_at: Optional[datetime] = None
    scheduled_for: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DraftResponse(BaseModel):
    id: str
    user_id: str
    bundle_id: str
    bundle_name: str
    topic: Optional[str]
    tone: str
    generated_html: str
    edited_html: Optional[str]
    status: str
    readiness_score: Optional[int]
    sources: List[str]
    created_at: datetime
    updated_at: datetime
    sent_at: Optional[datetime]
    scheduled_for: Optional[datetime]
    # Voice training metadata
    voice_training_used: Optional[bool] = False
    voice_samples_count: Optional[int] = 0
    generation_metadata: Optional[Dict[str, Any]] = None


class SendDraftRequest(BaseModel):
    recipients: List[str]
    subject: Optional[str] = None
    bundle_color: Optional[str] = None

