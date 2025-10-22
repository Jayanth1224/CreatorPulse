import time
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from functools import wraps
from app.database import SupabaseDB

logger = logging.getLogger(__name__)

class PerformanceService:
    """Service for monitoring and tracking performance metrics"""
    
    def __init__(self):
        self.db = SupabaseDB.get_service_client()
        self._metrics: Dict[str, Any] = {}
    
    def track_api_call(self, endpoint: str, method: str, duration: float, status_code: int, user_id: Optional[str] = None):
        """Track API call performance"""
        try:
            metric = {
                "endpoint": endpoint,
                "method": method,
                "duration_ms": round(duration * 1000, 2),
                "status_code": status_code,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat()
            }
            
            # Store in memory for quick access
            key = f"{endpoint}:{method}"
            if key not in self._metrics:
                self._metrics[key] = []
            self._metrics[key].append(metric)
            
            # Keep only last 100 entries per endpoint
            if len(self._metrics[key]) > 100:
                self._metrics[key] = self._metrics[key][-100:]
            
            logger.info(f"API Performance: {endpoint} {method} - {duration:.3f}s ({status_code})")
            
        except Exception as e:
            logger.error(f"Error tracking API performance: {str(e)}")
    
    def get_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance summary for the last N hours"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Aggregate metrics from memory
            summary = {
                "total_calls": 0,
                "avg_duration_ms": 0,
                "slow_calls": 0,
                "error_calls": 0,
                "endpoints": {}
            }
            
            all_durations = []
            all_calls = 0
            
            for endpoint, metrics in self._metrics.items():
                recent_metrics = [
                    m for m in metrics 
                    if datetime.fromisoformat(m["timestamp"]) >= cutoff_time
                ]
                
                if not recent_metrics:
                    continue
                
                durations = [m["duration_ms"] for m in recent_metrics]
                status_codes = [m["status_code"] for m in recent_metrics]
                
                endpoint_summary = {
                    "calls": len(recent_metrics),
                    "avg_duration_ms": round(sum(durations) / len(durations), 2),
                    "min_duration_ms": min(durations),
                    "max_duration_ms": max(durations),
                    "slow_calls": len([d for d in durations if d > 1000]),  # > 1 second
                    "error_calls": len([s for s in status_codes if s >= 400])
                }
                
                summary["endpoints"][endpoint] = endpoint_summary
                all_durations.extend(durations)
                all_calls += len(recent_metrics)
                summary["slow_calls"] += endpoint_summary["slow_calls"]
                summary["error_calls"] += endpoint_summary["error_calls"]
            
            if all_durations:
                summary["total_calls"] = all_calls
                summary["avg_duration_ms"] = round(sum(all_durations) / len(all_durations), 2)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting performance summary: {str(e)}")
            return {
                "total_calls": 0,
                "avg_duration_ms": 0,
                "slow_calls": 0,
                "error_calls": 0,
                "endpoints": {}
            }
    
    def get_slow_endpoints(self, threshold_ms: float = 1000) -> list:
        """Get endpoints that are slower than threshold"""
        slow_endpoints = []
        
        for endpoint, metrics in self._metrics.items():
            recent_metrics = metrics[-50:]  # Last 50 calls
            if not recent_metrics:
                continue
            
            avg_duration = sum(m["duration_ms"] for m in recent_metrics) / len(recent_metrics)
            if avg_duration > threshold_ms:
                slow_endpoints.append({
                    "endpoint": endpoint,
                    "avg_duration_ms": round(avg_duration, 2),
                    "calls": len(recent_metrics)
                })
        
        return sorted(slow_endpoints, key=lambda x: x["avg_duration_ms"], reverse=True)
    
    def clear_old_metrics(self, hours: int = 24):
        """Clear metrics older than specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for endpoint in list(self._metrics.keys()):
            self._metrics[endpoint] = [
                m for m in self._metrics[endpoint]
                if datetime.fromisoformat(m["timestamp"]) >= cutoff_time
            ]
            
            # Remove empty entries
            if not self._metrics[endpoint]:
                del self._metrics[endpoint]

# Global performance service instance
performance_service = PerformanceService()

def track_performance(endpoint: str, method: str = "GET"):
    """Decorator to track function performance"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                performance_service.track_api_call(endpoint, method, duration, 200)
                return result
            except Exception as e:
                duration = time.time() - start_time
                performance_service.track_api_call(endpoint, method, duration, 500)
                raise
        return async_wrapper
    
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            performance_service.track_api_call(endpoint, method, duration, 200)
            return result
        except Exception as e:
            duration = time.time() - start_time
            performance_service.track_api_call(endpoint, method, duration, 500)
            raise
    
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
