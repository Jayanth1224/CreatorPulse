from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from app.models.voice_training import (
    VoiceSampleCreate,
    VoiceSampleResponse,
    VoiceSampleUpdate,
    VoiceSamplesUploadRequest,
    VoiceSamplesUploadResponse,
    VoiceTrainingStatus
)
from app.services.voice_training_service import VoiceTrainingService
from app.utils.auth import get_current_user

router = APIRouter()
voice_training_service = VoiceTrainingService()


@router.post("/samples", response_model=VoiceSampleResponse)
async def create_voice_sample(
    sample_data: VoiceSampleCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new voice training sample"""
    try:
        user_id = current_user["id"]
        sample = voice_training_service.create_voice_sample(user_id, sample_data)
        return sample
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create voice sample: {str(e)}")


@router.post("/samples/upload", response_model=VoiceSamplesUploadResponse)
async def upload_voice_samples(
    upload_request: VoiceSamplesUploadRequest,
    current_user: dict = Depends(get_current_user)
):
    """Upload multiple voice training samples"""
    try:
        user_id = current_user["id"]
        samples = voice_training_service.bulk_create_samples(user_id, upload_request.samples)
        
        return VoiceSamplesUploadResponse(
            created_count=len(samples),
            sample_ids=[sample.id for sample in samples],
            message=f"Successfully uploaded {len(samples)} voice training samples"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload voice samples: {str(e)}")


@router.get("/samples", response_model=List[VoiceSampleResponse])
async def get_voice_samples(
    current_user: dict = Depends(get_current_user),
    limit: int = Query(20, ge=1, le=50, description="Maximum number of samples to return")
):
    """Get all voice training samples for the current user"""
    try:
        user_id = current_user["id"]
        samples = voice_training_service.get_user_voice_samples(user_id, limit)
        return samples
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get voice samples: {str(e)}")


@router.get("/samples/{sample_id}", response_model=VoiceSampleResponse)
async def get_voice_sample(
    sample_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific voice training sample"""
    try:
        user_id = current_user["id"]
        samples = voice_training_service.get_user_voice_samples(user_id, limit=100)
        
        # Find the specific sample
        sample = next((s for s in samples if s.id == sample_id), None)
        if not sample:
            raise HTTPException(status_code=404, detail="Voice sample not found")
        
        return sample
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get voice sample: {str(e)}")


@router.patch("/samples/{sample_id}", response_model=VoiceSampleResponse)
async def update_voice_sample(
    sample_id: str,
    update_data: VoiceSampleUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a voice training sample"""
    try:
        user_id = current_user["id"]
        sample = voice_training_service.update_voice_sample(user_id, sample_id, update_data)
        
        if not sample:
            raise HTTPException(status_code=404, detail="Voice sample not found")
        
        return sample
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update voice sample: {str(e)}")


@router.delete("/samples/{sample_id}")
async def delete_voice_sample(
    sample_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a voice training sample"""
    try:
        user_id = current_user["id"]
        success = voice_training_service.delete_voice_sample(user_id, sample_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Voice sample not found")
        
        return {"message": "Voice sample deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete voice sample: {str(e)}")


@router.get("/status", response_model=VoiceTrainingStatus)
async def get_voice_training_status(
    current_user: dict = Depends(get_current_user)
):
    """Get voice training status for the current user"""
    try:
        user_id = current_user["id"]
        status = voice_training_service.get_voice_training_status(user_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get voice training status: {str(e)}")


@router.post("/samples/clear")
async def clear_all_voice_samples(
    current_user: dict = Depends(get_current_user)
):
    """Clear all voice training samples for the current user"""
    try:
        user_id = current_user["id"]
        
        # Get all samples first to count them
        samples = voice_training_service.get_user_voice_samples(user_id, limit=1000)
        sample_count = len(samples)
        
        if sample_count == 0:
            return {"message": "No voice samples to clear", "cleared_count": 0}
        
        # Delete all samples
        for sample in samples:
            voice_training_service.delete_voice_sample(user_id, sample.id)
        
        return {
            "message": f"Successfully cleared {sample_count} voice samples",
            "cleared_count": sample_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear voice samples: {str(e)}")
