import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import hashlib
import time
import random

logger = logging.getLogger(__name__)


class TwitterService:
    """Service for scraping Twitter handles and extracting tweet content"""
    
    def __init__(self):
        self.cache = {}
        self.rate_limit_delay = 2  # seconds between requests
        self.max_retries = 3
        
    async def scrape_handle(self, handle: str, limit: int = 20) -> List[Dict]:
        """
        Scrape recent tweets from a Twitter handle
        
        Args:
            handle: Twitter handle (with or without @)
            limit: Maximum number of tweets to fetch
            
        Returns:
            List of tweet dictionaries in standardized format
        """
        try:
            # Clean handle (remove @ if present)
            clean_handle = handle.lstrip('@').lower()
            
            # Check cache first
            cache_key = f"twitter_{clean_handle}_{limit}"
            if cache_key in self.cache:
                cached_time, cached_data = self.cache[cache_key]
                if datetime.now() - cached_time < timedelta(minutes=30):
                    logger.info(f"[TWITTER] Using cached data for @{clean_handle}")
                    return cached_data
            
            logger.info(f"[TWITTER] Scraping tweets from @{clean_handle}")
            
            # Simulate Twitter scraping (replace with actual scraper)
            tweets = await self._simulate_twitter_scraping(clean_handle, limit)
            
            # Cache results
            self.cache[cache_key] = (datetime.now(), tweets)
            
            logger.info(f"[TWITTER] Scraped {len(tweets)} tweets from @{clean_handle}")
            return tweets
            
        except Exception as e:
            logger.error(f"[TWITTER] Failed to scrape @{handle}: {str(e)}")
            return []
    
    async def _simulate_twitter_scraping(self, handle: str, limit: int) -> List[Dict]:
        """
        Simulate Twitter scraping with mock data
        In production, this would use snscrape or similar library
        """
        # Simulate rate limiting
        await asyncio.sleep(random.uniform(1, 3))
        
        # Mock tweet data
        mock_tweets = [
            {
                "title": f"Tweet from @{handle} about AI developments",
                "link": f"https://twitter.com/{handle}/status/1234567890",
                "summary": "Exciting news about the latest AI breakthrough that could revolutionize the industry...",
                "published": datetime.now() - timedelta(hours=2),
                "author": f"@{handle}",
                "source_url": f"https://twitter.com/{handle}",
                "hash": hashlib.md5(f"tweet_{handle}_1234567890".encode()).hexdigest(),
                "metadata": {
                    "retweets": 45,
                    "likes": 234,
                    "replies": 12,
                    "type": "tweet"
                }
            },
            {
                "title": f"Thread from @{handle} on tech trends",
                "link": f"https://twitter.com/{handle}/status/1234567891",
                "summary": "A comprehensive thread about the future of technology and what to expect in 2024...",
                "published": datetime.now() - timedelta(hours=6),
                "author": f"@{handle}",
                "source_url": f"https://twitter.com/{handle}",
                "hash": hashlib.md5(f"tweet_{handle}_1234567891".encode()).hexdigest(),
                "metadata": {
                    "retweets": 89,
                    "likes": 456,
                    "replies": 23,
                    "type": "thread"
                }
            },
            {
                "title": f"Quick update from @{handle}",
                "link": f"https://twitter.com/{handle}/status/1234567892",
                "summary": "Just finished an amazing conference session. Key takeaways: 1) Innovation is accelerating 2) Collaboration is crucial 3) The future is bright!",
                "published": datetime.now() - timedelta(hours=12),
                "author": f"@{handle}",
                "source_url": f"https://twitter.com/{handle}",
                "hash": hashlib.md5(f"tweet_{handle}_1234567892".encode()).hexdigest(),
                "metadata": {
                    "retweets": 23,
                    "likes": 123,
                    "replies": 8,
                    "type": "tweet"
                }
            }
        ]
        
        return mock_tweets[:limit]
    
    def parse_tweet(self, tweet_data: Dict) -> Dict:
        """
        Parse raw tweet data into standardized format
        
        Args:
            tweet_data: Raw tweet data from scraper
            
        Returns:
            Standardized tweet dictionary
        """
        try:
            # Extract basic tweet information
            text = tweet_data.get('text', '')
            tweet_id = tweet_data.get('id', '')
            created_at = tweet_data.get('created_at', datetime.now())
            
            # Generate standardized entry
            entry = {
                "title": self._truncate_text(text, 100),
                "link": f"https://twitter.com/{tweet_data.get('user', {}).get('screen_name', '')}/status/{tweet_id}",
                "summary": text,
                "published": created_at,
                "author": f"@{tweet_data.get('user', {}).get('screen_name', '')}",
                "source_url": f"https://twitter.com/{tweet_data.get('user', {}).get('screen_name', '')}",
                "hash": self._generate_hash(tweet_id),
                "metadata": {
                    "retweets": tweet_data.get('retweet_count', 0),
                    "likes": tweet_data.get('favorite_count', 0),
                    "replies": tweet_data.get('reply_count', 0),
                    "type": "tweet"
                }
            }
            
            return entry
            
        except Exception as e:
            logger.error(f"[TWITTER] Failed to parse tweet: {str(e)}")
            return {}
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def _generate_hash(self, text: str) -> str:
        """Generate hash for deduplication"""
        return hashlib.md5(text.encode()).hexdigest()
    
    async def scrape_multiple_handles(self, handles: List[str], limit_per_handle: int = 20) -> List[Dict]:
        """
        Scrape multiple Twitter handles
        
        Args:
            handles: List of Twitter handles
            limit_per_handle: Maximum tweets per handle
            
        Returns:
            Aggregated list of tweets from all handles
        """
        all_tweets = []
        
        for handle in handles:
            try:
                tweets = await self.scrape_handle(handle, limit_per_handle)
                all_tweets.extend(tweets)
                
                # Rate limiting between handles
                await asyncio.sleep(self.rate_limit_delay)
                
            except Exception as e:
                logger.error(f"[TWITTER] Failed to scrape @{handle}: {str(e)}")
                continue
        
        # Deduplicate by hash
        seen_hashes = set()
        unique_tweets = []
        
        for tweet in all_tweets:
            if tweet.get("hash") not in seen_hashes:
                seen_hashes.add(tweet.get("hash"))
                unique_tweets.append(tweet)
        
        # Sort by published date (most recent first)
        unique_tweets.sort(
            key=lambda x: x.get("published", datetime.min),
            reverse=True
        )
        
        return unique_tweets[:50]  # Return top 50 most recent
    
    def score_tweets(self, tweets: List[Dict], topic: str = None) -> List[Dict]:
        """
        Score tweets based on engagement and recency
        
        Args:
            tweets: List of tweet dictionaries
            topic: Optional topic for relevance scoring
            
        Returns:
            Scored and sorted tweets
        """
        now = datetime.now()
        
        for tweet in tweets:
            # Recency score (0-1, exponential decay)
            pub_date = tweet.get("published", now - timedelta(days=7))
            hours_old = (now - pub_date).total_seconds() / 3600
            recency_score = max(0, 1 - (hours_old / 168))  # 1 week decay
            
            # Engagement score (0-1, based on likes/retweets)
            metadata = tweet.get("metadata", {})
            likes = metadata.get("likes", 0)
            retweets = metadata.get("retweets", 0)
            replies = metadata.get("replies", 0)
            
            engagement_score = min(1.0, (likes + retweets * 2 + replies) / 1000)
            
            # Relevance score (basic keyword matching if topic provided)
            relevance_score = 1.0
            if topic:
                topic_lower = topic.lower()
                title_lower = tweet.get("title", "").lower()
                summary_lower = tweet.get("summary", "").lower()
                
                if topic_lower in title_lower:
                    relevance_score = 1.5
                elif topic_lower in summary_lower:
                    relevance_score = 1.2
            
            # Twitter-specific weight (1.2x for real-time trends)
            twitter_weight = 1.2
            
            # Final score
            tweet["score"] = (recency_score * 0.4 + engagement_score * 0.4 + relevance_score * 0.2) * twitter_weight
        
        # Sort by score
        tweets.sort(key=lambda x: x.get("score", 0), reverse=True)
        return tweets
