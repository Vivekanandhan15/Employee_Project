from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio
from sqlalchemy.orm import Session
from database.database import SessionLocal
from services.cache_service import CacheService
from services.user_service import UserService
from services.department_service import DepartmentService
from services.user_department_service import UserDepartmentService


class BackgroundSyncService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def start(self):
        """Start the background sync service"""
        # Sync all users every 5 minutes
        self.scheduler.add_job(
            self.sync_all_users,
            trigger=IntervalTrigger(minutes=5),
            id="sync_all_users",
            name="Sync all users to cache"
        )

        # Sync all departments every 5 minutes
        self.scheduler.add_job(
            self.sync_all_departments,
            trigger=IntervalTrigger(minutes=5),
            id="sync_all_departments",
            name="Sync all departments to cache"
        )

        # Clean expired cache entries every 10 minutes
        self.scheduler.add_job(
            self.clean_expired_cache,
            trigger=IntervalTrigger(minutes=10),
            id="clean_expired_cache",
            name="Clean expired cache entries"
        )

        self.scheduler.start()

    def stop(self):
        """Stop the background sync service"""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=True)

    async def sync_all_users(self):
        """Sync all users from DB to cache"""
        db: Session = SessionLocal()
        try:
            users = await UserService.get_all_users(db)
            # Force refresh cache
            await CacheService.set_cached_all_users(users, ttl=300)
            print("Synced all users to cache")
        except Exception as e:
            print(f"Error syncing users: {e}")
        finally:
            db.close()

    async def sync_all_departments(self):
        """Sync all departments from DB to cache"""
        db: Session = SessionLocal()
        try:
            departments = await DepartmentService.get_all_departments(db)
            # Force refresh cache
            await CacheService.set_cached_all_departments(departments, ttl=300)
            print("Synced all departments to cache")
        except Exception as e:
            print(f"Error syncing departments: {e}")
        finally:
            db.close()

    async def clean_expired_cache(self):
        """Clean expired cache entries (Redis handles TTL automatically, but we can add custom cleanup)"""
        try:
            # Redis automatically expires keys with TTL, but we can log or add custom logic
            print("Cache cleanup check completed")
        except Exception as e:
            print(f"Error during cache cleanup: {e}")

    async def manual_invalidate_all_cache(self):
        """Manually invalidate all cache entries"""
        try:
            await CacheService.invalidate_user_cache()
            await CacheService.invalidate_department_cache()
            # Invalidate all user-department associations
            await CacheService.delete_pattern(f"{CacheService.USER_DEPARTMENT_PREFIX}*")
            print("Manually invalidated all cache")
        except Exception as e:
            print(f"Error invalidating cache: {e}")


# Global instance
background_sync = BackgroundSyncService()