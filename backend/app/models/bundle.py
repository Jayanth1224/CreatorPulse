from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union


class Source(BaseModel):
    type: str  # 'rss', 'twitter', 'youtube'
    value: str  # URL, @handle, or channel_id
    label: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BundleBase(BaseModel):
    key: str
    label: str
    description: str
    sources: List[Union[str, Source]] = []  # Support both old string format and new Source objects


class BundleCreate(BundleBase):
    is_preset: bool = False


class BundleUpdate(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None
    sources: Optional[List[Union[str, Source]]] = None


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
    sources: List[Union[str, Source]]  # Support both formats for backward compatibility

