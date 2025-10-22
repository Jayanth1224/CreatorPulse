import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.database import SupabaseDB
import statistics

logger = logging.getLogger(__name__)

class SpikeDetectionService:
    def __init__(self):
        self.db = SupabaseDB.get_service_client()
    
    async def detect_content_spikes(self, auto_newsletter_id: str, threshold: float = 2.0, timeframe_hours: int = 24) -> List[Dict[str, Any]]:
        """Detect content spikes for an auto-newsletter"""
        try:
            # Get the auto-newsletter configuration
            newsletter_res = self.db.table("auto_newsletters").select("*").eq("id", auto_newsletter_id).single().execute()
            if not newsletter_res.data:
                logger.error(f"Auto-newsletter {auto_newsletter_id} not found")
                return []
            
            newsletter = newsletter_res.data
            bundle_id = newsletter["bundle_id"]
            
            # Get sources for this bundle
            sources_res = self.db.table("sources").select("*").eq("bundle_id", bundle_id).execute()
            sources = sources_res.data or []
            
            spikes = []
            
            for source in sources:
                source_spikes = await self._detect_source_spikes(
                    source, threshold, timeframe_hours, auto_newsletter_id
                )
                spikes.extend(source_spikes)
            
            # Store detected spikes
            for spike in spikes:
                await self._store_spike_event(spike)
            
            return spikes
            
        except Exception as e:
            logger.error(f"Error detecting content spikes: {str(e)}")
            return []
    
    async def _detect_source_spikes(self, source: Dict[str, Any], threshold: float, timeframe_hours: int, auto_newsletter_id: str) -> List[Dict[str, Any]]:
        """Detect spikes for a specific source"""
        try:
            # Get content entries for this source in the specified timeframe
            cutoff_time = datetime.now() - timedelta(hours=timeframe_hours)
            
            entries_res = self.db.table("content_entries")\
                .select("*")\
                .eq("source_id", source["id"])\
                .gte("published_at", cutoff_time.isoformat())\
                .order("published_at", desc=True)\
                .execute()
            
            entries = entries_res.data or []
            
            if len(entries) < 3:  # Need at least 3 entries to detect spikes
                return []
            
            # Calculate engagement metrics
            engagement_scores = []
            for entry in entries:
                score = self._calculate_engagement_score(entry)
                engagement_scores.append(score)
            
            # Detect spikes using statistical analysis
            spikes = []
            if len(engagement_scores) >= 3:
                mean_score = statistics.mean(engagement_scores)
                std_dev = statistics.stdev(engagement_scores) if len(engagement_scores) > 1 else 0
                
                for i, (entry, score) in enumerate(zip(entries, engagement_scores)):
                    # Check if this entry is a spike
                    if std_dev > 0 and score > mean_score + (threshold * std_dev):
                        spike_data = {
                            "auto_newsletter_id": auto_newsletter_id,
                            "source_id": source["id"],
                            "spike_score": round(score, 3),
                            "spike_reason": f"Engagement spike: {score:.2f} vs mean {mean_score:.2f}",
                            "content_title": entry.get("title", ""),
                            "content_url": entry.get("link", ""),
                            "detected_at": datetime.now().isoformat(),
                            "processed": False
                        }
                        spikes.append(spike_data)
            
            return spikes
            
        except Exception as e:
            logger.error(f"Error detecting spikes for source {source.get('id')}: {str(e)}")
            return []
    
    def _calculate_engagement_score(self, entry: Dict[str, Any]) -> float:
        """Calculate engagement score for a content entry"""
        try:
            metadata = entry.get("metadata", {})
            
            # Base score from content age (newer = higher score)
            published_at = datetime.fromisoformat(entry.get("published_at", "").replace("Z", "+00:00"))
            age_hours = (datetime.now(published_at.tzinfo) - published_at).total_seconds() / 3600
            recency_score = max(0, 10 - age_hours)  # Higher score for newer content
            
            # Engagement metrics (if available)
            engagement_score = 0
            if "engagement" in metadata:
                engagement = metadata["engagement"]
                engagement_score = (
                    engagement.get("likes", 0) * 0.1 +
                    engagement.get("shares", 0) * 0.3 +
                    engagement.get("comments", 0) * 0.2 +
                    engagement.get("views", 0) * 0.001
                )
            
            # Signal score from source
            signal_score = entry.get("signal_score", 1.0)
            
            # Combine scores
            total_score = (recency_score * 0.4 + engagement_score * 0.4 + signal_score * 0.2)
            
            return round(total_score, 3)
            
        except Exception as e:
            logger.error(f"Error calculating engagement score: {str(e)}")
            return 0.0
    
    async def _store_spike_event(self, spike_data: Dict[str, Any]):
        """Store spike event in database"""
        try:
            self.db.table("spike_events").insert(spike_data).execute()
            logger.info(f"Stored spike event for source {spike_data['source_id']}")
            
        except Exception as e:
            logger.error(f"Error storing spike event: {str(e)}")
    
    async def get_unprocessed_spikes(self, auto_newsletter_id: str) -> List[Dict[str, Any]]:
        """Get unprocessed spike events for an auto-newsletter"""
        try:
            res = self.db.table("spike_events")\
                .select("*")\
                .eq("auto_newsletter_id", auto_newsletter_id)\
                .eq("processed", False)\
                .order("detected_at", desc=True)\
                .execute()
            
            return res.data or []
            
        except Exception as e:
            logger.error(f"Error getting unprocessed spikes: {str(e)}")
            return []
    
    async def mark_spike_processed(self, spike_id: str):
        """Mark a spike event as processed"""
        try:
            self.db.table("spike_events")\
                .update({"processed": True})\
                .eq("id", spike_id)\
                .execute()
            
            logger.info(f"Marked spike event {spike_id} as processed")
            
        except Exception as e:
            logger.error(f"Error marking spike as processed: {str(e)}")
    
    async def get_spike_analytics(self, auto_newsletter_id: str, days: int = 30) -> Dict[str, Any]:
        """Get spike analytics for an auto-newsletter"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Get all spikes in the time period
            res = self.db.table("spike_events")\
                .select("*")\
                .eq("auto_newsletter_id", auto_newsletter_id)\
                .gte("detected_at", cutoff_date.isoformat())\
                .execute()
            
            spikes = res.data or []
            
            if not spikes:
                return {
                    "total_spikes": 0,
                    "avg_spike_score": 0,
                    "top_sources": [],
                    "spike_trend": "stable"
                }
            
            # Calculate analytics
            total_spikes = len(spikes)
            avg_spike_score = sum(spike["spike_score"] for spike in spikes) / total_spikes
            
            # Top sources by spike count
            source_counts = {}
            for spike in spikes:
                source_id = spike["source_id"]
                source_counts[source_id] = source_counts.get(source_id, 0) + 1
            
            top_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Calculate spike trend (comparing first half vs second half)
            mid_point = len(spikes) // 2
            first_half_avg = sum(spike["spike_score"] for spike in spikes[:mid_point]) / mid_point if mid_point > 0 else 0
            second_half_avg = sum(spike["spike_score"] for spike in spikes[mid_point:]) / (len(spikes) - mid_point) if len(spikes) - mid_point > 0 else 0
            
            if second_half_avg > first_half_avg * 1.1:
                spike_trend = "increasing"
            elif second_half_avg < first_half_avg * 0.9:
                spike_trend = "decreasing"
            else:
                spike_trend = "stable"
            
            return {
                "total_spikes": total_spikes,
                "avg_spike_score": round(avg_spike_score, 3),
                "top_sources": [{"source_id": source_id, "spike_count": count} for source_id, count in top_sources],
                "spike_trend": spike_trend
            }
            
        except Exception as e:
            logger.error(f"Error getting spike analytics: {str(e)}")
            return {
                "total_spikes": 0,
                "avg_spike_score": 0,
                "top_sources": [],
                "spike_trend": "stable"
            }
