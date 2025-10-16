import feedparser
from typing import List, Dict
from datetime import datetime, timedelta
import hashlib


class RSSService:
    """Service for parsing and aggregating RSS feeds"""
    
    def __init__(self):
        self.cache = {}
    
    def parse_feed(self, feed_url: str, timeout: int = 10) -> List[Dict]:
        """Parse a single RSS feed and return entries"""
        try:
            import socket
            socket.setdefaulttimeout(timeout)
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:  # Feed parsing error
                print(f"Warning: Error parsing feed {feed_url}")
                return []
            
            entries = []
            for entry in feed.entries[:20]:  # Limit to 20 most recent
                entries.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", entry.get("description", "")),
                    "published": self._parse_date(entry),
                    "author": entry.get("author", ""),
                    "source_url": feed_url,
                    "hash": self._generate_hash(entry.get("link", entry.get("title", "")))
                })
            
            return entries
        
        except Exception as e:
            print(f"Error parsing feed {feed_url}: {str(e)}")
            return []
    
    def parse_multiple_feeds(self, feed_urls: List[str]) -> List[Dict]:
        """Parse multiple RSS feeds and return aggregated entries"""
        all_entries = []
        
        for url in feed_urls:
            if url:  # Skip empty URLs
                entries = self.parse_feed(url)
                all_entries.extend(entries)
        
        # Deduplicate by hash
        seen_hashes = set()
        unique_entries = []
        
        for entry in all_entries:
            if entry["hash"] not in seen_hashes:
                seen_hashes.add(entry["hash"])
                unique_entries.append(entry)
        
        # Sort by published date (most recent first)
        unique_entries.sort(
            key=lambda x: x.get("published", datetime.min),
            reverse=True
        )
        
        return unique_entries[:30]  # Return top 30 most recent
    
    def filter_recent_entries(self, entries: List[Dict], days: int = 7) -> List[Dict]:
        """Filter entries to only include those from the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        return [
            entry for entry in entries
            if entry.get("published", datetime.min) >= cutoff_date
        ]
    
    def score_entries(self, entries: List[Dict], topic: str = None) -> List[Dict]:
        """Score entries based on recency and relevance"""
        now = datetime.now()
        
        for entry in entries:
            # Recency score (0-1, exponential decay)
            pub_date = entry.get("published", now - timedelta(days=30))
            days_old = (now - pub_date).days
            recency_score = max(0, 1 - (days_old / 30))
            
            # Relevance score (basic keyword matching if topic provided)
            relevance_score = 1.0
            if topic:
                topic_lower = topic.lower()
                title_lower = entry.get("title", "").lower()
                summary_lower = entry.get("summary", "").lower()
                
                if topic_lower in title_lower:
                    relevance_score = 1.5
                elif topic_lower in summary_lower:
                    relevance_score = 1.2
            
            entry["score"] = recency_score * relevance_score
        
        entries.sort(key=lambda x: x.get("score", 0), reverse=True)
        return entries
    
    def _parse_date(self, entry) -> datetime:
        """Parse published date from entry"""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            try:
                return datetime(*entry.published_parsed[:6])
            except:
                pass
        
        if hasattr(entry, "updated_parsed") and entry.updated_parsed:
            try:
                return datetime(*entry.updated_parsed[:6])
            except:
                pass
        
        return datetime.now()
    
    def _generate_hash(self, text: str) -> str:
        """Generate hash for deduplication"""
        return hashlib.md5(text.encode()).hexdigest()

