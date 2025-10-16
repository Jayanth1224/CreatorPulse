"""
Background RSS Crawler Service
Periodically crawls RSS feeds and stores entries in database
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.rss_service import RSSService
from app.database import get_db
from datetime import datetime
import hashlib
import logging

logger = logging.getLogger(__name__)


class RSSCrawler:
    """Background service for crawling RSS feeds"""
    
    def __init__(self):
        self.rss_service = RSSService()
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
    
    def start(self):
        """Start the background crawler"""
        if self.is_running:
            logger.warning("RSS Crawler is already running")
            return
        
        # Schedule crawling every 6 hours
        self.scheduler.add_job(
            self.crawl_all_feeds,
            trigger=IntervalTrigger(hours=6),
            id='rss_crawler',
            name='Crawl RSS feeds',
            replace_existing=True
        )
        
        # Also run immediately on startup
        self.scheduler.add_job(
            self.crawl_all_feeds,
            id='initial_crawl',
            name='Initial RSS crawl'
        )
        
        self.scheduler.start()
        self.is_running = True
        logger.info("RSS Crawler started")
    
    def stop(self):
        """Stop the background crawler"""
        if not self.is_running:
            return
        
        self.scheduler.shutdown(wait=False)
        self.is_running = False
        logger.info("RSS Crawler stopped")
    
    async def crawl_all_feeds(self):
        """Crawl all active RSS feeds and store entries"""
        try:
            logger.info("[RSS CRAWLER] Starting feed crawl...")
            
            db = get_db()
            
            # Get all active sources
            sources_response = db.table("sources").select("*").eq("is_active", True).execute()
            sources = sources_response.data
            
            if not sources:
                logger.info("[RSS CRAWLER] No active sources found")
                return
            
            logger.info(f"[RSS CRAWLER] Found {len(sources)} active sources")
            
            total_entries = 0
            total_new_entries = 0
            
            for source in sources:
                try:
                    # Parse the feed
                    entries = self.rss_service.parse_feed(source['feed_url'])
                    total_entries += len(entries)
                    
                    # Store entries in database
                    new_count = await self._store_entries(entries, source['id'])
                    total_new_entries += new_count
                    
                    # Update last_crawled timestamp
                    db.table("sources").update({
                        "last_crawled": datetime.now().isoformat()
                    }).eq("id", source['id']).execute()
                    
                    logger.info(f"[RSS CRAWLER] Processed {len(entries)} entries from {source['feed_url']} ({new_count} new)")
                
                except Exception as e:
                    logger.error(f"[RSS CRAWLER] Failed to crawl {source['feed_url']}: {str(e)}")
                    continue
            
            logger.info(f"[RSS CRAWLER] Crawl complete. Processed {total_entries} entries, {total_new_entries} new")
            
            # Clean up expired entries
            await self._cleanup_expired_entries()
        
        except Exception as e:
            logger.error(f"[RSS CRAWLER] Crawl failed: {str(e)}")
    
    async def _store_entries(self, entries: list, source_id: str) -> int:
        """Store RSS entries in database, skipping duplicates"""
        db = get_db()
        new_count = 0
        
        for entry in entries:
            try:
                # Create content hash for deduplication
                content_hash = self._generate_content_hash(entry)
                
                # Check if entry already exists
                existing = db.table("rss_entries").select("id").eq("content_hash", content_hash).execute()
                if existing.data:
                    continue  # Skip duplicate
                
                # Prepare entry data
                entry_data = {
                    "source_id": source_id,
                    "title": entry.get("title", "")[:500],  # Limit title length
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", "")[:2000],  # Limit summary length
                    "published_at": entry.get("published_parsed"),
                    "author": entry.get("author", "")[:200],
                    "content_hash": content_hash
                }
                
                # Insert into database
                db.table("rss_entries").insert(entry_data).execute()
                new_count += 1
            
            except Exception as e:
                logger.error(f"[RSS CRAWLER] Failed to store entry: {str(e)}")
                continue
        
        return new_count
    
    def _generate_content_hash(self, entry: dict) -> str:
        """Generate unique hash for entry to detect duplicates"""
        content = f"{entry.get('title', '')}{entry.get('link', '')}"
        return hashlib.md5(content.encode()).hexdigest()
    
    async def _cleanup_expired_entries(self):
        """Remove expired RSS entries from database"""
        try:
            db = get_db()
            
            # Call the cleanup function
            db.rpc("cleanup_expired_rss_entries").execute()
            
            logger.info("[RSS CRAWLER] Cleaned up expired entries")
        except Exception as e:
            logger.error(f"[RSS CRAWLER] Cleanup failed: {str(e)}")
    
    async def crawl_bundle_feeds(self, bundle_id: str) -> dict:
        """Manually trigger crawl for a specific bundle's feeds"""
        try:
            db = get_db()
            
            # Get bundle
            bundle_response = db.table("bundles").select("*").eq("id", bundle_id).execute()
            if not bundle_response.data:
                return {"success": False, "error": "Bundle not found"}
            
            bundle = bundle_response.data[0]
            feed_urls = bundle.get("sources", [])
            
            if not feed_urls:
                return {"success": False, "error": "No sources in bundle"}
            
            # Parse feeds
            entries = self.rss_service.parse_multiple_feeds(feed_urls)
            
            return {
                "success": True,
                "entries_count": len(entries),
                "bundle_id": bundle_id
            }
        
        except Exception as e:
            logger.error(f"[RSS CRAWLER] Bundle crawl failed: {str(e)}")
            return {"success": False, "error": str(e)}


# Global crawler instance
rss_crawler = RSSCrawler()

