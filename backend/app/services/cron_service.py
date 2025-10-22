import asyncio
import logging
from datetime import datetime
from .auto_newsletter_service import AutoNewsletterService

logger = logging.getLogger(__name__)

class CronService:
    def __init__(self):
        self.is_running = False
        self.task = None
    
    async def start(self):
        """Start the cron service"""
        if self.is_running:
            logger.warning("Cron service is already running")
            return
        
        self.is_running = True
        self.task = asyncio.create_task(self._run_cron_job())
        logger.info("Cron service started")
    
    async def stop(self):
        """Stop the cron service"""
        if not self.is_running:
            logger.warning("Cron service is not running")
            return
        
        self.is_running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        logger.info("Cron service stopped")
    
    async def _run_cron_job(self):
        """Main cron job loop"""
        while self.is_running:
            try:
                await self._process_auto_newsletters()
                
                # Wait for 1 minute before next check
                await asyncio.sleep(60)
                
            except asyncio.CancelledError:
                logger.info("Cron job cancelled")
                break
            except Exception as e:
                logger.error(f"Error in cron job: {str(e)}")
                # Wait 5 minutes before retrying on error
                await asyncio.sleep(300)
    
    async def _process_auto_newsletters(self):
        """Process all auto-newsletters that are due for generation"""
        try:
            service = AutoNewsletterService()
            await service.process_scheduled_newsletters()
            
            logger.debug("Processed auto-newsletters")
            
        except Exception as e:
            logger.error(f"Failed to process auto-newsletters: {str(e)}")
        finally:
            pass

# Global cron service instance
cron_service = CronService()
