from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AnalyticsBase(BaseModel):
    draft_id: str


class AnalyticsCreate(AnalyticsBase):
    sent_at: datetime
    opened_at: Optional[datetime] = None
    clicked_at: Optional[datetime] = None


class Analytics(AnalyticsBase):
    id: str
    sent_at: datetime
    opened_at: Optional[datetime] = None
    clicked_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AnalyticsSummary(BaseModel):
    open_rate: float
    click_through_rate: float
    avg_review_time: float
    draft_acceptance_rate: float
    total_drafts: int
    total_sent: int

