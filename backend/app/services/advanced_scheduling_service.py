import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.database import SupabaseDB
import pytz
import json

logger = logging.getLogger(__name__)

class AdvancedSchedulingService:
    def __init__(self):
        self.db = SupabaseDB.get_service_client()
    
    async def create_custom_schedule(
        self,
        auto_newsletter_id: str,
        schedule_type: str,
        schedule_config: Dict[str, Any],
        timezone: str = "America/Los_Angeles"
    ) -> Dict[str, Any]:
        """Create a custom schedule for an auto-newsletter"""
        try:
            # Validate timezone
            if timezone not in pytz.all_timezones:
                raise ValueError(f"Invalid timezone: {timezone}")
            
            # Validate schedule configuration
            if not self._validate_schedule_config(schedule_type, schedule_config):
                raise ValueError(f"Invalid schedule configuration for type: {schedule_type}")
            
            # Create custom schedule object
            custom_schedule = {
                "type": schedule_type,
                "config": schedule_config,
                "timezone": timezone,
                "created_at": datetime.now().isoformat()
            }
            
            # Update auto-newsletter with custom schedule
            update_data = {
                "custom_schedule": custom_schedule,
                "timezone": timezone,
                "schedule_enabled": True
            }
            
            res = self.db.table("auto_newsletters")\
                .update(update_data)\
                .eq("id", auto_newsletter_id)\
                .execute()
            
            if not res.data:
                raise Exception("Failed to update auto-newsletter with custom schedule")
            
            logger.info(f"Created custom schedule for auto-newsletter {auto_newsletter_id}")
            return res.data[0]
            
        except Exception as e:
            logger.error(f"Error creating custom schedule: {str(e)}")
            raise
    
    def _validate_schedule_config(self, schedule_type: str, config: Dict[str, Any]) -> bool:
        """Validate schedule configuration based on type"""
        try:
            if schedule_type == "interval":
                # Interval-based scheduling (e.g., every 2 hours)
                required_fields = ["interval_hours", "start_time"]
                return all(field in config for field in required_fields)
            
            elif schedule_type == "business_hours":
                # Business hours scheduling (e.g., 9 AM - 5 PM, weekdays only)
                required_fields = ["start_hour", "end_hour", "days_of_week"]
                return all(field in config for field in required_fields)
            
            elif schedule_type == "content_based":
                # Content-based scheduling (triggered by content spikes)
                required_fields = ["spike_threshold", "max_frequency_hours"]
                return all(field in config for field in required_fields)
            
            elif schedule_type == "trend_based":
                # Trend-based scheduling (triggered by trending topics)
                required_fields = ["trend_keywords", "trend_threshold"]
                return all(field in config for field in required_fields)
            
            elif schedule_type == "custom_cron":
                # Custom cron expression
                required_fields = ["cron_expression"]
                return all(field in config for field in required_fields)
            
            return False
            
        except Exception as e:
            logger.error(f"Error validating schedule config: {str(e)}")
            return False
    
    async def get_next_scheduled_time(self, auto_newsletter_id: str) -> Optional[datetime]:
        """Get the next scheduled time for an auto-newsletter"""
        try:
            # Get auto-newsletter configuration
            res = self.db.table("auto_newsletters").select("*").eq("id", auto_newsletter_id).single().execute()
            if not res.data:
                return None
            
            newsletter = res.data
            
            if not newsletter.get("schedule_enabled", True):
                return None
            
            # Check if custom schedule exists
            custom_schedule = newsletter.get("custom_schedule")
            if custom_schedule:
                return await self._calculate_custom_schedule_time(custom_schedule)
            else:
                return await self._calculate_standard_schedule_time(newsletter)
            
        except Exception as e:
            logger.error(f"Error getting next scheduled time: {str(e)}")
            return None
    
    async def _calculate_custom_schedule_time(self, custom_schedule: Dict[str, Any]) -> Optional[datetime]:
        """Calculate next time based on custom schedule"""
        try:
            schedule_type = custom_schedule.get("type")
            config = custom_schedule.get("config", {})
            timezone_str = custom_schedule.get("timezone", "America/Los_Angeles")
            
            tz = pytz.timezone(timezone_str)
            now = datetime.now(tz)
            
            if schedule_type == "interval":
                return await self._calculate_interval_schedule(now, config, tz)
            elif schedule_type == "business_hours":
                return await self._calculate_business_hours_schedule(now, config, tz)
            elif schedule_type == "content_based":
                return await self._calculate_content_based_schedule(now, config, tz)
            elif schedule_type == "trend_based":
                return await self._calculate_trend_based_schedule(now, config, tz)
            elif schedule_type == "custom_cron":
                return await self._calculate_cron_schedule(now, config, tz)
            
            return None
            
        except Exception as e:
            logger.error(f"Error calculating custom schedule time: {str(e)}")
            return None
    
    async def _calculate_interval_schedule(self, now: datetime, config: Dict[str, Any], tz) -> datetime:
        """Calculate next time for interval-based scheduling"""
        interval_hours = config.get("interval_hours", 24)
        start_time_str = config.get("start_time", "08:00")
        
        # Parse start time
        start_hour, start_minute = map(int, start_time_str.split(':'))
        
        # Create start time for today
        start_today = now.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
        
        # If start time has passed today, calculate next occurrence
        if now >= start_today:
            next_time = start_today + timedelta(hours=interval_hours)
        else:
            next_time = start_today
        
        return next_time
    
    async def _calculate_business_hours_schedule(self, now: datetime, config: Dict[str, Any], tz) -> datetime:
        """Calculate next time for business hours scheduling"""
        start_hour = config.get("start_hour", 9)
        end_hour = config.get("end_hour", 17)
        days_of_week = config.get("days_of_week", [1, 2, 3, 4, 5])  # Monday-Friday
        
        # Find next business day and time
        current_day = now.weekday() + 1  # Convert to 1-7 format
        current_hour = now.hour
        
        # If current day is a business day and within business hours
        if current_day in days_of_week and start_hour <= current_hour < end_hour:
            # Schedule for next business day
            days_ahead = 1
            while (current_day + days_ahead - 1) % 7 + 1 not in days_of_week:
                days_ahead += 1
            next_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0) + timedelta(days=days_ahead)
        else:
            # Find next business day
            days_ahead = 0
            while (current_day + days_ahead - 1) % 7 + 1 not in days_of_week:
                days_ahead += 1
            next_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0) + timedelta(days=days_ahead)
        
        return next_time
    
    async def _calculate_content_based_schedule(self, now: datetime, config: Dict[str, Any], tz) -> Optional[datetime]:
        """Calculate next time for content-based scheduling"""
        # This would typically be triggered by spike detection
        # For now, return None (will be handled by spike detection service)
        return None
    
    async def _calculate_trend_based_schedule(self, now: datetime, config: Dict[str, Any], tz) -> Optional[datetime]:
        """Calculate next time for trend-based scheduling"""
        # This would typically be triggered by trend detection
        # For now, return None (will be handled by trend detection service)
        return None
    
    async def _calculate_cron_schedule(self, now: datetime, config: Dict[str, Any], tz) -> Optional[datetime]:
        """Calculate next time for cron-based scheduling"""
        # This would require a cron parser library
        # For now, return None (would need croniter library)
        return None
    
    async def _calculate_standard_schedule_time(self, newsletter: Dict[str, Any]) -> Optional[datetime]:
        """Calculate next time for standard scheduling"""
        try:
            timezone_str = newsletter.get("timezone", "America/Los_Angeles")
            tz = pytz.timezone(timezone_str)
            now = datetime.now(tz)
            
            schedule_time = newsletter.get("schedule_time", "08:00:00")
            frequency = newsletter.get("schedule_frequency", "daily")
            schedule_day = newsletter.get("schedule_day")
            
            # Parse schedule time
            time_parts = schedule_time.split(':')
            hour = int(time_parts[0])
            minute = int(time_parts[1]) if len(time_parts) > 1 else 0
            
            # Create today's scheduled time
            scheduled_today = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            if frequency == "daily":
                if now >= scheduled_today:
                    return scheduled_today + timedelta(days=1)
                else:
                    return scheduled_today
            
            elif frequency == "weekly" and schedule_day:
                # Find next occurrence of the specified day
                days_ahead = (schedule_day - now.weekday() - 1) % 7
                if days_ahead == 0 and now >= scheduled_today:
                    days_ahead = 7
                return scheduled_today + timedelta(days=days_ahead)
            
            elif frequency == "monthly" and schedule_day:
                # Find next occurrence of the specified day of month
                if now.day >= schedule_day and now >= scheduled_today:
                    # Next month
                    if now.month == 12:
                        next_month = now.replace(year=now.year + 1, month=1, day=schedule_day)
                    else:
                        next_month = now.replace(month=now.month + 1, day=schedule_day)
                    return next_month
                else:
                    # This month
                    return now.replace(day=schedule_day)
            
            return None
            
        except Exception as e:
            logger.error(f"Error calculating standard schedule time: {str(e)}")
            return None
    
    async def get_scheduled_newsletters(self, current_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get all newsletters that should be generated at the current time"""
        try:
            if current_time is None:
                current_time = datetime.now()
            
            # Get all active newsletters
            res = self.db.table("auto_newsletters")\
                .select("*")\
                .eq("is_active", True)\
                .eq("schedule_enabled", True)\
                .execute()
            
            newsletters = res.data or []
            due_newsletters = []
            
            for newsletter in newsletters:
                next_time = await self.get_next_scheduled_time(newsletter["id"])
                if next_time and next_time <= current_time:
                    due_newsletters.append(newsletter)
            
            return due_newsletters
            
        except Exception as e:
            logger.error(f"Error getting scheduled newsletters: {str(e)}")
            return []
    
    async def get_schedule_analytics(self, auto_newsletter_id: str, days: int = 30) -> Dict[str, Any]:
        """Get scheduling analytics for an auto-newsletter"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Get analytics data
            res = self.db.table("auto_newsletter_analytics")\
                .select("*")\
                .eq("auto_newsletter_id", auto_newsletter_id)\
                .gte("generation_time", cutoff_date.isoformat())\
                .execute()
            
            analytics = res.data or []
            
            if not analytics:
                return {
                    "total_generations": 0,
                    "avg_generation_interval": 0,
                    "schedule_adherence": 0,
                    "timezone_accuracy": 0
                }
            
            # Calculate metrics
            total_generations = len(analytics)
            
            # Calculate average generation interval
            if total_generations > 1:
                intervals = []
                for i in range(1, total_generations):
                    prev_time = datetime.fromisoformat(analytics[i-1]["generation_time"])
                    curr_time = datetime.fromisoformat(analytics[i]["generation_time"])
                    intervals.append((curr_time - prev_time).total_seconds() / 3600)  # hours
                avg_interval = sum(intervals) / len(intervals)
            else:
                avg_interval = 0
            
            # Calculate schedule adherence (how often it runs on time)
            # This would require comparing actual vs expected times
            schedule_adherence = 0.85  # Placeholder
            
            # Calculate timezone accuracy
            timezone_accuracy = 0.95  # Placeholder
            
            return {
                "total_generations": total_generations,
                "avg_generation_interval": round(avg_interval, 2),
                "schedule_adherence": round(schedule_adherence, 3),
                "timezone_accuracy": round(timezone_accuracy, 3)
            }
            
        except Exception as e:
            logger.error(f"Error getting schedule analytics: {str(e)}")
            return {
                "total_generations": 0,
                "avg_generation_interval": 0,
                "schedule_adherence": 0,
                "timezone_accuracy": 0
            }
