import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.database import SupabaseDB
import statistics

logger = logging.getLogger(__name__)

class AutoNewsletterAnalyticsService:
    def __init__(self):
        self.db = SupabaseDB.get_service_client()
    
    async def track_newsletter_generation(
        self,
        auto_newsletter_id: str,
        draft_id: str,
        content_quality_score: Optional[float] = None,
        trend_relevance_score: Optional[float] = None,
        spike_impact_score: Optional[float] = None,
        total_sources_used: int = 0,
        unique_trends_detected: int = 0,
        spike_events_processed: int = 0
    ) -> Dict[str, Any]:
        """Track analytics for a newsletter generation"""
        try:
            analytics_data = {
                "auto_newsletter_id": auto_newsletter_id,
                "draft_id": draft_id,
                "generation_time": datetime.now().isoformat(),
                "content_quality_score": content_quality_score,
                "trend_relevance_score": trend_relevance_score,
                "spike_impact_score": spike_impact_score,
                "total_sources_used": total_sources_used,
                "unique_trends_detected": unique_trends_detected,
                "spike_events_processed": spike_events_processed
            }
            
            res = self.db.table("auto_newsletter_analytics").insert(analytics_data).execute()
            
            if not res.data:
                raise Exception("Failed to insert analytics data")
            
            logger.info(f"Tracked analytics for auto-newsletter {auto_newsletter_id}")
            return res.data[0]
            
        except Exception as e:
            logger.error(f"Error tracking newsletter generation: {str(e)}")
            raise
    
    async def get_newsletter_performance(self, auto_newsletter_id: str, days: int = 30) -> Dict[str, Any]:
        """Get performance metrics for an auto-newsletter"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Get analytics data
            analytics_res = self.db.table("auto_newsletter_analytics")\
                .select("*")\
                .eq("auto_newsletter_id", auto_newsletter_id)\
                .gte("generation_time", cutoff_date.isoformat())\
                .execute()
            
            analytics = analytics_res.data or []
            
            if not analytics:
                return {
                    "total_generations": 0,
                    "avg_content_quality": 0,
                    "avg_trend_relevance": 0,
                    "avg_spike_impact": 0,
                    "total_sources_used": 0,
                    "total_trends_detected": 0,
                    "total_spikes_processed": 0,
                    "performance_trend": "stable"
                }
            
            # Calculate metrics
            total_generations = len(analytics)
            
            # Content quality metrics
            quality_scores = [a["content_quality_score"] for a in analytics if a["content_quality_score"] is not None]
            avg_content_quality = statistics.mean(quality_scores) if quality_scores else 0
            
            # Trend relevance metrics
            trend_scores = [a["trend_relevance_score"] for a in analytics if a["trend_relevance_score"] is not None]
            avg_trend_relevance = statistics.mean(trend_scores) if trend_scores else 0
            
            # Spike impact metrics
            spike_scores = [a["spike_impact_score"] for a in analytics if a["spike_impact_score"] is not None]
            avg_spike_impact = statistics.mean(spike_scores) if spike_scores else 0
            
            # Source usage metrics
            total_sources_used = sum(a["total_sources_used"] for a in analytics)
            total_trends_detected = sum(a["unique_trends_detected"] for a in analytics)
            total_spikes_processed = sum(a["spike_events_processed"] for a in analytics)
            
            # Performance trend (comparing first half vs second half)
            if len(analytics) >= 4:
                mid_point = len(analytics) // 2
                first_half_quality = statistics.mean([a["content_quality_score"] for a in analytics[:mid_point] if a["content_quality_score"] is not None])
                second_half_quality = statistics.mean([a["content_quality_score"] for a in analytics[mid_point:] if a["content_quality_score"] is not None])
                
                if second_half_quality > first_half_quality * 1.05:
                    performance_trend = "improving"
                elif second_half_quality < first_half_quality * 0.95:
                    performance_trend = "declining"
                else:
                    performance_trend = "stable"
            else:
                performance_trend = "stable"
            
            return {
                "total_generations": total_generations,
                "avg_content_quality": round(avg_content_quality, 3),
                "avg_trend_relevance": round(avg_trend_relevance, 3),
                "avg_spike_impact": round(avg_spike_impact, 3),
                "total_sources_used": total_sources_used,
                "total_trends_detected": total_trends_detected,
                "total_spikes_processed": total_spikes_processed,
                "performance_trend": performance_trend
            }
            
        except Exception as e:
            logger.error(f"Error getting newsletter performance: {str(e)}")
            return {
                "total_generations": 0,
                "avg_content_quality": 0,
                "avg_trend_relevance": 0,
                "avg_spike_impact": 0,
                "total_sources_used": 0,
                "total_trends_detected": 0,
                "total_spikes_processed": 0,
                "performance_trend": "stable"
            }
    
    async def get_trend_analytics(self, auto_newsletter_id: str, days: int = 30) -> Dict[str, Any]:
        """Get trend analytics for an auto-newsletter"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Get trend data
            trend_res = self.db.table("trend_data")\
                .select("*")\
                .gte("data_date", cutoff_date.date().isoformat())\
                .order("trend_score", desc=True)\
                .execute()
            
            trends = trend_res.data or []
            
            if not trends:
                return {
                    "total_trends": 0,
                    "avg_trend_score": 0,
                    "top_trending_keywords": [],
                    "trend_volatility": 0,
                    "trend_diversity": 0
                }
            
            # Calculate metrics
            total_trends = len(trends)
            avg_trend_score = statistics.mean([t["trend_score"] for t in trends])
            
            # Top trending keywords
            keyword_scores = {}
            for trend in trends:
                keyword = trend["keyword"]
                if keyword not in keyword_scores:
                    keyword_scores[keyword] = []
                keyword_scores[keyword].append(trend["trend_score"])
            
            # Average scores per keyword
            keyword_avg_scores = {k: statistics.mean(scores) for k, scores in keyword_scores.items()}
            top_keywords = sorted(keyword_avg_scores.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Trend volatility (standard deviation of trend scores)
            trend_scores = [t["trend_score"] for t in trends]
            trend_volatility = statistics.stdev(trend_scores) if len(trend_scores) > 1 else 0
            
            # Trend diversity (number of unique keywords)
            unique_keywords = len(set(t["keyword"] for t in trends))
            trend_diversity = unique_keywords / total_trends if total_trends > 0 else 0
            
            return {
                "total_trends": total_trends,
                "avg_trend_score": round(avg_trend_score, 3),
                "top_trending_keywords": [{"keyword": k, "avg_score": v} for k, v in top_keywords],
                "trend_volatility": round(trend_volatility, 3),
                "trend_diversity": round(trend_diversity, 3)
            }
            
        except Exception as e:
            logger.error(f"Error getting trend analytics: {str(e)}")
            return {
                "total_trends": 0,
                "avg_trend_score": 0,
                "top_trending_keywords": [],
                "trend_volatility": 0,
                "trend_diversity": 0
            }
    
    async def get_spike_analytics(self, auto_newsletter_id: str, days: int = 30) -> Dict[str, Any]:
        """Get spike analytics for an auto-newsletter"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Get spike events
            spike_res = self.db.table("spike_events")\
                .select("*")\
                .eq("auto_newsletter_id", auto_newsletter_id)\
                .gte("detected_at", cutoff_date.isoformat())\
                .execute()
            
            spikes = spike_res.data or []
            
            if not spikes:
                return {
                    "total_spikes": 0,
                    "avg_spike_score": 0,
                    "spike_frequency": 0,
                    "top_spike_sources": [],
                    "spike_impact": 0
                }
            
            # Calculate metrics
            total_spikes = len(spikes)
            avg_spike_score = statistics.mean([s["spike_score"] for s in spikes])
            
            # Spike frequency (spikes per day)
            spike_frequency = total_spikes / days
            
            # Top spike sources
            source_counts = {}
            for spike in spikes:
                source_id = spike["source_id"]
                source_counts[source_id] = source_counts.get(source_id, 0) + 1
            
            top_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Spike impact (average score weighted by frequency)
            spike_impact = avg_spike_score * spike_frequency
            
            return {
                "total_spikes": total_spikes,
                "avg_spike_score": round(avg_spike_score, 3),
                "spike_frequency": round(spike_frequency, 3),
                "top_spike_sources": [{"source_id": s, "spike_count": c} for s, c in top_sources],
                "spike_impact": round(spike_impact, 3)
            }
            
        except Exception as e:
            logger.error(f"Error getting spike analytics: {str(e)}")
            return {
                "total_spikes": 0,
                "avg_spike_score": 0,
                "spike_frequency": 0,
                "top_spike_sources": [],
                "spike_impact": 0
            }
    
    async def get_comprehensive_analytics(self, auto_newsletter_id: str, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive analytics combining all metrics"""
        try:
            # Get all analytics data
            performance = await self.get_newsletter_performance(auto_newsletter_id, days)
            trend_analytics = await self.get_trend_analytics(auto_newsletter_id, days)
            spike_analytics = await self.get_spike_analytics(auto_newsletter_id, days)
            
            # Calculate overall health score
            health_score = self._calculate_health_score(performance, trend_analytics, spike_analytics)
            
            # Generate insights
            insights = self._generate_insights(performance, trend_analytics, spike_analytics)
            
            return {
                "health_score": health_score,
                "performance": performance,
                "trend_analytics": trend_analytics,
                "spike_analytics": spike_analytics,
                "insights": insights,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting comprehensive analytics: {str(e)}")
            return {
                "health_score": 0,
                "performance": {},
                "trend_analytics": {},
                "spike_analytics": {},
                "insights": [],
                "generated_at": datetime.now().isoformat()
            }
    
    def _calculate_health_score(self, performance: Dict, trend_analytics: Dict, spike_analytics: Dict) -> float:
        """Calculate overall health score for the auto-newsletter"""
        try:
            # Weight different metrics
            content_quality = performance.get("avg_content_quality", 0)
            trend_relevance = performance.get("avg_trend_relevance", 0)
            spike_impact = performance.get("avg_spike_impact", 0)
            
            # Normalize scores (assuming 0-1 range)
            health_score = (
                content_quality * 0.4 +
                trend_relevance * 0.3 +
                spike_impact * 0.3
            )
            
            return round(min(max(health_score, 0), 1), 3)
            
        except Exception as e:
            logger.error(f"Error calculating health score: {str(e)}")
            return 0.0
    
    def _generate_insights(self, performance: Dict, trend_analytics: Dict, spike_analytics: Dict) -> List[str]:
        """Generate actionable insights based on analytics"""
        insights = []
        
        try:
            # Content quality insights
            content_quality = performance.get("avg_content_quality", 0)
            if content_quality < 0.5:
                insights.append("Content quality is below average. Consider improving source selection or content generation prompts.")
            elif content_quality > 0.8:
                insights.append("Excellent content quality! Your source selection and content generation are working well.")
            
            # Trend relevance insights
            trend_relevance = performance.get("avg_trend_relevance", 0)
            if trend_relevance < 0.3:
                insights.append("Low trend relevance detected. Consider adding more trending keywords to your bundle.")
            elif trend_relevance > 0.7:
                insights.append("Great trend relevance! Your content is well-aligned with current trends.")
            
            # Spike impact insights
            spike_impact = performance.get("avg_spike_impact", 0)
            if spike_impact < 0.2:
                insights.append("Low spike impact. Consider enabling spike detection to capture viral content.")
            elif spike_impact > 0.6:
                insights.append("High spike impact! Your content is effectively capturing viral moments.")
            
            # Trend diversity insights
            trend_diversity = trend_analytics.get("trend_diversity", 0)
            if trend_diversity < 0.3:
                insights.append("Low trend diversity. Consider expanding your keyword coverage.")
            elif trend_diversity > 0.7:
                insights.append("Good trend diversity! You're covering a wide range of trending topics.")
            
            # Performance trend insights
            performance_trend = performance.get("performance_trend", "stable")
            if performance_trend == "improving":
                insights.append("Performance is improving! Keep up the good work.")
            elif performance_trend == "declining":
                insights.append("Performance is declining. Consider reviewing your configuration.")
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return ["Unable to generate insights at this time."]
