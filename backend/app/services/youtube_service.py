import logging
from typing import List, Dict, Optional
from datetime import datetime
import re
from urllib.parse import urlparse, parse_qs

from app.services.rss_service import RSSService

logger = logging.getLogger(__name__)


class YouTubeService:
    """Service for parsing YouTube channel RSS feeds"""
    
    def __init__(self):
        self.rss_service = RSSService()
        self.base_rss_url = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        
    def get_channel_rss_url(self, channel_id: str) -> str:
        """
        Generate YouTube RSS URL for a channel
        
        Args:
            channel_id: YouTube channel ID
            
        Returns:
            RSS URL for the channel
        """
        return self.base_rss_url.format(channel_id=channel_id)
    
    def extract_channel_id_from_url(self, url: str) -> Optional[str]:
        """
        Extract channel ID from various YouTube URL formats
        
        Args:
            url: YouTube channel URL
            
        Returns:
            Channel ID or None if not found
        """
        try:
            # Handle different YouTube URL formats
            patterns = [
                r'youtube\.com/channel/([a-zA-Z0-9_-]+)',
                r'youtube\.com/c/([a-zA-Z0-9_-]+)',
                r'youtube\.com/@([a-zA-Z0-9_-]+)',
                r'youtube\.com/user/([a-zA-Z0-9_-]+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(1)
            
            # If it's already a channel ID
            if re.match(r'^[a-zA-Z0-9_-]+$', url):
                return url
                
            return None
            
        except Exception as e:
            logger.error(f"[YOUTUBE] Failed to extract channel ID from {url}: {str(e)}")
            return None
    
    async def parse_channel_feed(self, channel_identifier: str) -> List[Dict]:
        """
        Parse YouTube channel RSS feed
        
        Args:
            channel_identifier: Channel ID or YouTube URL
            
        Returns:
            List of video entries in standardized format
        """
        try:
            # Extract channel ID if URL provided
            channel_id = self.extract_channel_id_from_url(channel_identifier)
            if not channel_id:
                logger.error(f"[YOUTUBE] Invalid channel identifier: {channel_identifier}")
                return []
            
            # Generate RSS URL
            rss_url = self.get_channel_rss_url(channel_id)
            logger.info(f"[YOUTUBE] Parsing channel {channel_id} RSS feed")
            
            # Use existing RSS service to parse the feed
            entries = self.rss_service.parse_feed(rss_url)
            
            # Transform entries to YouTube-specific format
            youtube_entries = []
            for entry in entries:
                youtube_entry = self._transform_to_youtube_format(entry, channel_id)
                if youtube_entry:
                    youtube_entries.append(youtube_entry)
            
            logger.info(f"[YOUTUBE] Parsed {len(youtube_entries)} videos from channel {channel_id}")
            return youtube_entries
            
        except Exception as e:
            logger.error(f"[YOUTUBE] Failed to parse channel {channel_identifier}: {str(e)}")
            return []
    
    def _transform_to_youtube_format(self, entry: Dict, channel_id: str) -> Optional[Dict]:
        """
        Transform RSS entry to YouTube-specific format
        
        Args:
            entry: RSS entry from feedparser
            channel_id: YouTube channel ID
            
        Returns:
            YouTube-formatted entry or None if invalid
        """
        try:
            # Extract video ID from link
            video_id = self._extract_video_id(entry.get("link", ""))
            if not video_id:
                return None
            
            # Create YouTube-specific entry
            youtube_entry = {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", ""),
                "published": entry.get("published", datetime.now()),
                "author": entry.get("author", ""),
                "source_url": f"https://www.youtube.com/channel/{channel_id}",
                "hash": entry.get("hash", ""),
                "metadata": {
                    "video_id": video_id,
                    "channel_id": channel_id,
                    "type": "video",
                    "platform": "youtube"
                }
            }
            
            return youtube_entry
            
        except Exception as e:
            logger.error(f"[YOUTUBE] Failed to transform entry: {str(e)}")
            return None
    
    def _extract_video_id(self, video_url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            Video ID or None if not found
        """
        try:
            # Handle different YouTube URL formats
            patterns = [
                r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
                r'youtu\.be/([a-zA-Z0-9_-]+)',
                r'youtube\.com/embed/([a-zA-Z0-9_-]+)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, video_url)
                if match:
                    return match.group(1)
            
            return None
            
        except Exception as e:
            logger.error(f"[YOUTUBE] Failed to extract video ID from {video_url}: {str(e)}")
            return None
    
    async def parse_multiple_channels(self, channel_identifiers: List[str], limit_per_channel: int = 20) -> List[Dict]:
        """
        Parse multiple YouTube channels
        
        Args:
            channel_identifiers: List of channel IDs or URLs
            limit_per_channel: Maximum videos per channel
            
        Returns:
            Aggregated list of videos from all channels
        """
        all_videos = []
        
        for channel_id in channel_identifiers:
            try:
                videos = await self.parse_channel_feed(channel_id)
                all_videos.extend(videos[:limit_per_channel])
                
            except Exception as e:
                logger.error(f"[YOUTUBE] Failed to parse channel {channel_id}: {str(e)}")
                continue
        
        # Deduplicate by hash
        seen_hashes = set()
        unique_videos = []
        
        for video in all_videos:
            if video.get("hash") not in seen_hashes:
                seen_hashes.add(video.get("hash"))
                unique_videos.append(video)
        
        # Sort by published date (most recent first)
        unique_videos.sort(
            key=lambda x: x.get("published", datetime.min),
            reverse=True
        )
        
        return unique_videos[:50]  # Return top 50 most recent
    
    def score_videos(self, videos: List[Dict], topic: str = None) -> List[Dict]:
        """
        Score videos based on recency and relevance
        
        Args:
            videos: List of video dictionaries
            topic: Optional topic for relevance scoring
            
        Returns:
            Scored and sorted videos
        """
        from datetime import timedelta
        
        now = datetime.now()
        
        for video in videos:
            # Recency score (0-1, exponential decay)
            pub_date = video.get("published", now - timedelta(days=7))
            hours_old = (now - pub_date).total_seconds() / 3600
            recency_score = max(0, 1 - (hours_old / 168))  # 1 week decay
            
            # Relevance score (basic keyword matching if topic provided)
            relevance_score = 1.0
            if topic:
                topic_lower = topic.lower()
                title_lower = video.get("title", "").lower()
                summary_lower = video.get("summary", "").lower()
                
                if topic_lower in title_lower:
                    relevance_score = 1.5
                elif topic_lower in summary_lower:
                    relevance_score = 1.2
            
            # YouTube-specific weight (1.0x for video content)
            youtube_weight = 1.0
            
            # Final score
            video["score"] = (recency_score * 0.6 + relevance_score * 0.4) * youtube_weight
        
        # Sort by score
        videos.sort(key=lambda x: x.get("score", 0), reverse=True)
        return videos
    
    def validate_channel(self, channel_identifier: str) -> bool:
        """
        Validate if a channel identifier is valid
        
        Args:
            channel_identifier: Channel ID or YouTube URL
            
        Returns:
            True if valid, False otherwise
        """
        try:
            channel_id = self.extract_channel_id_from_url(channel_identifier)
            return channel_id is not None
            
        except Exception as e:
            logger.error(f"[YOUTUBE] Failed to validate channel {channel_identifier}: {str(e)}")
            return False
