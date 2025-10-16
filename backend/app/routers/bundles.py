from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.bundle import Bundle, BundleResponse
from app.database import get_db, SupabaseDB
import json

router = APIRouter()

# Keep PRESET_BUNDLES for backward compatibility with draft_generator
PRESET_BUNDLES = []  # Will be loaded from DB


def load_preset_bundles_from_db():
    """Load preset bundles from database"""
    try:
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        response = db.table("bundles").select("*").eq("is_preset", True).execute()
        return response.data
    except Exception as e:
        print(f"[ERROR] Failed to load preset bundles: {str(e)}")
        return []


@router.get("/presets", response_model=List[BundleResponse])
async def get_preset_bundles():
    """Get all preset bundles"""
    try:
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        response = db.table("bundles").select("*").eq("is_preset", True).execute()
        return response.data
    except Exception as e:
        print(f"[ERROR] Failed to fetch preset bundles: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch bundles: {str(e)}")


@router.get("/", response_model=List[BundleResponse])
async def get_all_bundles(user_id: str = None):
    """Get all bundles (presets + user custom bundles)"""
    try:
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        
        if user_id:
            # Get presets and user's custom bundles
            response = db.table("bundles").select("*").or_(f"is_preset.eq.true,user_id.eq.{user_id}").execute()
        else:
            # Just get presets
            response = db.table("bundles").select("*").eq("is_preset", True).execute()
        
        return response.data
    except Exception as e:
        print(f"[ERROR] Failed to fetch bundles: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch bundles: {str(e)}")


@router.get("/{bundle_id}", response_model=BundleResponse)
async def get_bundle(bundle_id: str):
    """Get a specific bundle by ID"""
    try:
        db = SupabaseDB.get_service_client()  # Use service role to bypass RLS
        response = db.table("bundles").select("*").eq("id", bundle_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Bundle not found")
        
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to fetch bundle: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch bundle: {str(e)}")


# Load preset bundles into memory for draft_generator compatibility
PRESET_BUNDLES = load_preset_bundles_from_db()

