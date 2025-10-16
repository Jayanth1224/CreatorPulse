from pydantic import BaseModel
from typing import List, Optional


class BundleBase(BaseModel):
    key: str
    label: str
    description: str
    sources: List[str] = []


class BundleCreate(BundleBase):
    is_preset: bool = False


class BundleUpdate(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None
    sources: Optional[List[str]] = None


class Bundle(BundleBase):
    id: str
    is_preset: bool
    user_id: Optional[str] = None
    
    class Config:
        from_attributes = True


class BundleResponse(BaseModel):
    id: str
    key: str
    label: str
    description: str
    is_preset: bool
    sources: List[str]

