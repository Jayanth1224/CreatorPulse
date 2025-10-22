from fastapi import APIRouter, Depends, HTTPException
from app.services.performance_service import performance_service
from app.utils.auth import get_current_user
from typing import Dict, Any

router = APIRouter()

@router.get("/metrics")
async def get_performance_metrics(
    hours: int = 24,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get performance metrics for the last N hours"""
    try:
        return performance_service.get_performance_summary(hours)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get performance metrics: {str(e)}")

@router.get("/slow-endpoints")
async def get_slow_endpoints(
    threshold_ms: float = 1000,
    current_user: dict = Depends(get_current_user)
) -> list:
    """Get endpoints that are slower than threshold"""
    try:
        return performance_service.get_slow_endpoints(threshold_ms)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get slow endpoints: {str(e)}")

@router.post("/clear-metrics")
async def clear_old_metrics(
    hours: int = 24,
    current_user: dict = Depends(get_current_user)
) -> Dict[str, str]:
    """Clear performance metrics older than specified hours"""
    try:
        performance_service.clear_old_metrics(hours)
        return {"message": f"Cleared metrics older than {hours} hours"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear metrics: {str(e)}")
