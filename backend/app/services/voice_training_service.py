from typing import List, Dict, Optional
from datetime import datetime
from app.database import SupabaseDB
from app.models.voice_training import (
    VoiceSampleCreate, 
    VoiceSampleResponse, 
    VoiceSampleUpdate,
    VoiceTrainingStatus
)
import uuid


class VoiceTrainingService:
    """Service for managing user voice training samples"""
    
    def __init__(self):
        self.db = SupabaseDB.get_service_client()  # Use service client to bypass RLS
    
    def create_voice_sample(
        self, 
        user_id: str, 
        sample_data: VoiceSampleCreate
    ) -> VoiceSampleResponse:
        """Create a new voice training sample"""
        
        sample_id = str(uuid.uuid4())
        
        # Insert into database
        try:
            result = self.db.table("user_voice_samples").insert({
                "id": sample_id,
                "user_id": user_id,
                "title": sample_data.title,
                "content": sample_data.content
            }).execute()
            
            if not result.data:
                raise Exception("Failed to create voice sample")
        except Exception as e:
            print(f"Database error creating voice sample: {e}")
            raise Exception(f"Database error: {str(e)}")
        
        # Return the created sample
        return VoiceSampleResponse(
            id=sample_id,
            user_id=user_id,
            title=sample_data.title,
            content=sample_data.content,
            created_at=datetime.fromisoformat(result.data[0]["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(result.data[0]["updated_at"].replace("Z", "+00:00"))
        )
    
    def get_user_voice_samples(
        self, 
        user_id: str, 
        limit: int = 20
    ) -> List[VoiceSampleResponse]:
        """Get all voice samples for a user, ordered by most recent"""
        
        result = self.db.table("user_voice_samples")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        
        if not result.data:
            return []
        
        return [
            VoiceSampleResponse(
                id=sample["id"],
                user_id=sample["user_id"],
                title=sample["title"],
                content=sample["content"],
                created_at=datetime.fromisoformat(sample["created_at"].replace("Z", "+00:00")),
                updated_at=datetime.fromisoformat(sample["updated_at"].replace("Z", "+00:00"))
            )
            for sample in result.data
        ]
    
    def get_voice_samples_for_training(
        self, 
        user_id: str, 
        max_samples: int = 5
    ) -> List[Dict[str, str]]:
        """Get voice samples formatted for AI training (most recent and diverse)"""
        
        # Get the most recent samples
        samples = self.get_user_voice_samples(user_id, limit=max_samples)
        
        # Format for AI training
        return [
            {
                "title": sample.title,
                "content": sample.content
            }
            for sample in samples
        ]
    
    def update_voice_sample(
        self, 
        user_id: str, 
        sample_id: str, 
        update_data: VoiceSampleUpdate
    ) -> Optional[VoiceSampleResponse]:
        """Update a voice sample"""
        
        # Build update dict with only provided fields
        update_dict = {}
        if update_data.title is not None:
            update_dict["title"] = update_data.title
        if update_data.content is not None:
            update_dict["content"] = update_data.content
        
        if not update_dict:
            return None
        
        result = self.db.table("user_voice_samples")\
            .update(update_dict)\
            .eq("id", sample_id)\
            .eq("user_id", user_id)\
            .execute()
        
        if not result.data:
            return None
        
        sample = result.data[0]
        return VoiceSampleResponse(
            id=sample["id"],
            user_id=sample["user_id"],
            title=sample["title"],
            content=sample["content"],
            created_at=datetime.fromisoformat(sample["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(sample["updated_at"].replace("Z", "+00:00"))
        )
    
    def delete_voice_sample(
        self, 
        user_id: str, 
        sample_id: str
    ) -> bool:
        """Delete a voice sample"""
        
        result = self.db.table("user_voice_samples")\
            .delete()\
            .eq("id", sample_id)\
            .eq("user_id", user_id)\
            .execute()
        
        return len(result.data) > 0
    
    def get_voice_training_status(
        self, 
        user_id: str
    ) -> VoiceTrainingStatus:
        """Get voice training status for a user"""
        
        # Get sample count and last updated
        result = self.db.table("user_voice_samples")\
            .select("created_at, updated_at")\
            .eq("user_id", user_id)\
            .order("updated_at", desc=True)\
            .limit(1)\
            .execute()
        
        has_samples = len(result.data) > 0
        sample_count = len(result.data) if has_samples else 0
        last_updated = None
        
        if has_samples and result.data:
            last_updated = datetime.fromisoformat(result.data[0]["updated_at"].replace("Z", "+00:00"))
        
        return VoiceTrainingStatus(
            has_samples=has_samples,
            sample_count=sample_count,
            last_updated=last_updated,
            is_active=has_samples and sample_count >= 3  # Need at least 3 samples for effective training
        )
    
    def bulk_create_samples(
        self, 
        user_id: str, 
        samples: List[VoiceSampleCreate]
    ) -> List[VoiceSampleResponse]:
        """Create multiple voice samples in bulk"""
        
        if len(samples) > 50:
            raise ValueError("Cannot create more than 50 samples at once")
        
        # Prepare data for bulk insert
        sample_data = []
        for sample in samples:
            sample_data.append({
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "title": sample.title,
                "content": sample.content
            })
        
        # Bulk insert
        result = self.db.table("user_voice_samples")\
            .insert(sample_data)\
            .execute()
        
        if not result.data:
            raise Exception("Failed to create voice samples")
        
        # Return created samples
        return [
            VoiceSampleResponse(
                id=sample["id"],
                user_id=sample["user_id"],
                title=sample["title"],
                content=sample["content"],
                created_at=datetime.fromisoformat(sample["created_at"].replace("Z", "+00:00")),
                updated_at=datetime.fromisoformat(sample["updated_at"].replace("Z", "+00:00"))
            )
            for sample in result.data
        ]
