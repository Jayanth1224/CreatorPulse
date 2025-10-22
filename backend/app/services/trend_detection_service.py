import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.database import SupabaseDB
from app.config import settings
import json

logger = logging.getLogger(__name__)

class TrendDetectionService:
    def __init__(self):
        self.db = SupabaseDB.get_service_client()
        self.firecrawl_api_key = settings.firecrawl_api_key
        self.google_trends_api_key = settings.google_trends_api_key
    
    async def detect_trends_for_keywords(self, keywords: List[str], region: str = "US") -> List[Dict[str, Any]]:
        """Detect trending topics for given keywords"""
        trends = []
        
        for keyword in keywords:
            try:
                # Get Google Trends data
                trend_score = await self._get_google_trends_score(keyword, region)
                
                # Get Firecrawl data for additional context
                firecrawl_data = await self._get_firecrawl_trend_data(keyword)
                
                trend_data = {
                    "keyword": keyword,
                    "trend_score": trend_score,
                    "source": "google_trends",
                    "region": region,
                    "data_date": datetime.now().date(),
                    "firecrawl_data": firecrawl_data
                }
                
                trends.append(trend_data)
                
                # Store in database
                await self._store_trend_data(trend_data)
                
            except Exception as e:
                logger.error(f"Error detecting trends for keyword '{keyword}': {str(e)}")
                continue
        
        return trends
    
    async def _get_google_trends_score(self, keyword: str, region: str) -> float:
        """Get trend score from Google Trends (simulated for now)"""
        # In a real implementation, you would use the Google Trends API
        # For now, we'll simulate trend data
        import random
        return round(random.uniform(0.1, 10.0), 2)
    
    async def _get_firecrawl_trend_data(self, keyword: str) -> Dict[str, Any]:
        """Get trend data from Firecrawl API v2"""
        if not self.firecrawl_api_key:
            logger.warning("Firecrawl API key not configured")
            return {}
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.firecrawl_api_key}",
                    "Content-Type": "application/json"
                }
                
                # Use Firecrawl v2 search API
                search_url = "https://api.firecrawl.dev/v2/search"
                payload = {
                    "query": keyword,
                    "sources": ["news"],
                    "limit": 10
                }
                
                async with session.post(search_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Handle v2 API response format
                        results = data.get("data", [])
                        return {
                            "total_results": data.get("total", len(results)),
                            "recent_articles": len(results),
                            "trending_topics": [item.get("title", "") for item in results[:5]]
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Firecrawl API error: {response.status} - {error_text}")
                        return {}
        
        except Exception as e:
            logger.error(f"Error fetching Firecrawl data: {str(e)}")
            return {}
    
    async def _store_trend_data(self, trend_data: Dict[str, Any]):
        """Store trend data in database"""
        try:
            data = {
                "keyword": trend_data["keyword"],
                "trend_score": trend_data["trend_score"],
                "source": trend_data["source"],
                "region": trend_data["region"],
                "data_date": trend_data["data_date"].isoformat()
            }
            
            self.db.table("trend_data").insert(data).execute()
            logger.info(f"Stored trend data for keyword: {trend_data['keyword']}")
            
        except Exception as e:
            logger.error(f"Error storing trend data: {str(e)}")
    
    async def get_trending_keywords(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get currently trending keywords"""
        try:
            # Get keywords with highest trend scores from the last 24 hours
            yesterday = datetime.now() - timedelta(days=1)
            
            res = self.db.table("trend_data")\
                .select("keyword, trend_score, source, region")\
                .gte("data_date", yesterday.date().isoformat())\
                .order("trend_score", desc=True)\
                .limit(limit)\
                .execute()
            
            return res.data or []
            
        except Exception as e:
            logger.error(f"Error getting trending keywords: {str(e)}")
            return []
    
    async def analyze_trend_relevance(self, content: str, keywords: List[str]) -> float:
        """Analyze how relevant content is to current trends"""
        try:
            # Get current trend scores for keywords
            trending_keywords = await self.get_trending_keywords(50)
            trend_scores = {item["keyword"]: item["trend_score"] for item in trending_keywords}
            
            # Calculate relevance score based on keyword matches and trend scores
            relevance_score = 0.0
            content_lower = content.lower()
            
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    trend_score = trend_scores.get(keyword, 0)
                    relevance_score += trend_score
            
            # Normalize score (0-1)
            max_possible_score = sum(trend_scores.values())
            if max_possible_score > 0:
                relevance_score = min(relevance_score / max_possible_score, 1.0)
            
            return round(relevance_score, 3)
            
        except Exception as e:
            logger.error(f"Error analyzing trend relevance: {str(e)}")
            return 0.0
