from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.models.bundle import Bundle, BundleResponse, Source
from app.database import get_db, SupabaseDB
import json
import re

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


@router.post("/{bundle_id}/sources")
async def add_source_to_bundle(bundle_id: str, source: Source):
    """Add a source to a bundle"""
    try:
        db = SupabaseDB.get_service_client()
        
        # Validate source format
        if not _validate_source(source):
            raise HTTPException(status_code=400, detail="Invalid source format")
        
        # Check if bundle exists
        bundle_response = db.table("bundles").select("*").eq("id", bundle_id).execute()
        if not bundle_response.data:
            raise HTTPException(status_code=404, detail="Bundle not found")
        
        # Create source in database
        source_data = {
            "bundle_id": bundle_id,
            "type": source.type,
            "source_identifier": source.value,
            "label": source.label,
            "metadata": source.metadata or {}
        }
        
        result = db.table("sources").insert(source_data).execute()
        
        return {"success": True, "source_id": result.data[0]["id"]}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to add source to bundle: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to add source: {str(e)}")


@router.delete("/{bundle_id}/sources/{source_id}")
async def remove_source_from_bundle(bundle_id: str, source_id: str):
    """Remove a source from a bundle"""
    try:
        db = SupabaseDB.get_service_client()
        
        # Check if source exists and belongs to bundle
        source_response = db.table("sources").select("*").eq("id", source_id).eq("bundle_id", bundle_id).execute()
        if not source_response.data:
            raise HTTPException(status_code=404, detail="Source not found")
        
        # Delete source
        db.table("sources").delete().eq("id", source_id).execute()
        
        return {"success": True}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to remove source: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to remove source: {str(e)}")


@router.get("/{bundle_id}/sources")
async def get_bundle_sources(bundle_id: str):
    """Get all sources for a bundle"""
    try:
        db = SupabaseDB.get_service_client()
        
        # Check if bundle exists
        bundle_response = db.table("bundles").select("*").eq("id", bundle_id).execute()
        if not bundle_response.data:
            raise HTTPException(status_code=404, detail="Bundle not found")
        
        # Get sources
        sources_response = db.table("sources").select("*").eq("bundle_id", bundle_id).execute()
        
        return sources_response.data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to fetch bundle sources: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch sources: {str(e)}")


@router.post("/sources/validate")
async def validate_source(source: Source):
    """Validate a source format"""
    try:
        is_valid = _validate_source(source)
        return {"valid": is_valid}
        
    except Exception as e:
        print(f"[ERROR] Failed to validate source: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to validate source: {str(e)}")


def _validate_source(source: Source) -> bool:
    """Validate source format based on type"""
    try:
        if source.type == "rss":
            # Validate RSS URL
            return _is_valid_url(source.value)
        elif source.type == "twitter":
            # Validate Twitter handle
            return _is_valid_twitter_handle(source.value)
        elif source.type == "youtube":
            # Validate YouTube channel identifier
            return _is_valid_youtube_identifier(source.value)
        else:
            return False
    except:
        return False


def _is_valid_url(url: str) -> bool:
    """Check if string is a valid URL"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None


def _is_valid_twitter_handle(handle: str) -> bool:
    """Check if string is a valid Twitter handle"""
    # Remove @ if present
    clean_handle = handle.lstrip('@')
    # Twitter handles: 1-15 characters, alphanumeric and underscore only
    return bool(re.match(r'^[a-zA-Z0-9_]{1,15}$', clean_handle))


def _is_valid_youtube_identifier(identifier: str) -> bool:
    """Check if string is a valid YouTube channel identifier"""
    # YouTube channel IDs: 24 characters, alphanumeric and some special chars
    if re.match(r'^[a-zA-Z0-9_-]{24}$', identifier):
        return True
    
    # YouTube channel URLs
    url_patterns = [
        r'youtube\.com/channel/[a-zA-Z0-9_-]+',
        r'youtube\.com/c/[a-zA-Z0-9_-]+',
        r'youtube\.com/@[a-zA-Z0-9_-]+',
        r'youtube\.com/user/[a-zA-Z0-9_-]+',
    ]
    
    for pattern in url_patterns:
        if re.search(pattern, identifier):
            return True
    
    return False

