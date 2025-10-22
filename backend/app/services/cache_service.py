import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from app.database import SupabaseDB

logger = logging.getLogger(__name__)

class CacheService:
    """Simple in-memory cache service for analytics and other frequently accessed data"""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl: Dict[str, datetime] = {}
        self.db = SupabaseDB.get_service_client()
    
    def _get_cache_key(self, user_id: str, cache_type: str, **kwargs) -> str:
        """Generate cache key from user_id, cache_type, and additional parameters"""
        key_parts = [user_id, cache_type]
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        return ":".join(key_parts)
    
    def _is_cache_valid(self, cache_key: str, ttl_seconds: int = 300) -> bool:
        """Check if cache entry is still valid"""
        if cache_key not in self._cache_ttl:
            return False
        
        cache_time = self._cache_ttl[cache_key]
        return datetime.now() < cache_time + timedelta(seconds=ttl_seconds)
    
    def get(self, cache_key: str, ttl_seconds: int = 300) -> Optional[Any]:
        """Get cached data if valid"""
        if cache_key in self._cache and self._is_cache_valid(cache_key, ttl_seconds):
            logger.debug(f"Cache hit for key: {cache_key}")
            return self._cache[cache_key]
        
        if cache_key in self._cache:
            logger.debug(f"Cache expired for key: {cache_key}")
            del self._cache[cache_key]
            del self._cache_ttl[cache_key]
        
        return None
    
    def set(self, cache_key: str, data: Any, ttl_seconds: int = 300) -> None:
        """Set cached data with TTL"""
        self._cache[cache_key] = data
        self._cache_ttl[cache_key] = datetime.now()
        logger.debug(f"Cached data for key: {cache_key} (TTL: {ttl_seconds}s)")
    
    def invalidate(self, user_id: str, cache_type: str) -> None:
        """Invalidate all cache entries for a user and cache type"""
        keys_to_remove = []
        pattern = f"{user_id}:{cache_type}"
        
        for key in self._cache.keys():
            if key.startswith(pattern):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            if key in self._cache:
                del self._cache[key]
            if key in self._cache_ttl:
                del self._cache_ttl[key]
        
        logger.debug(f"Invalidated {len(keys_to_remove)} cache entries for pattern: {pattern}")
    
    def clear_all(self) -> None:
        """Clear all cached data"""
        self._cache.clear()
        self._cache_ttl.clear()
        logger.info("Cleared all cache entries")
    
    async def get_analytics_summary(self, user_id: str, ttl_seconds: int = 300) -> Optional[Dict[str, Any]]:
        """Get cached analytics summary"""
        cache_key = self._get_cache_key(user_id, "analytics_summary")
        return self.get(cache_key, ttl_seconds)
    
    async def set_analytics_summary(self, user_id: str, data: Dict[str, Any], ttl_seconds: int = 300) -> None:
        """Cache analytics summary"""
        cache_key = self._get_cache_key(user_id, "analytics_summary")
        self.set(cache_key, data, ttl_seconds)
    
    async def get_drafts_list(self, user_id: str, status: Optional[str] = None, ttl_seconds: int = 60) -> Optional[list]:
        """Get cached drafts list"""
        cache_key = self._get_cache_key(user_id, "drafts_list", status=status or "all")
        return self.get(cache_key, ttl_seconds)
    
    async def set_drafts_list(self, user_id: str, data: list, status: Optional[str] = None, ttl_seconds: int = 60) -> None:
        """Cache drafts list"""
        cache_key = self._get_cache_key(user_id, "drafts_list", status=status or "all")
        self.set(cache_key, data, ttl_seconds)
    
    async def invalidate_user_cache(self, user_id: str) -> None:
        """Invalidate all cache entries for a user"""
        self.invalidate(user_id, "analytics_summary")
        self.invalidate(user_id, "drafts_list")
        logger.info(f"Invalidated all cache entries for user: {user_id}")

# Global cache instance
cache_service = CacheService()
