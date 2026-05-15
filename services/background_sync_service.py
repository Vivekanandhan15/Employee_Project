from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from database.database import SessionLocal
from services.cache_service import CacheService
from models.user import User
from models.department import Department
from core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BackgroundSyncService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.last_sync_users = None
        self.last_sync_departments = None

    def start(self):
        """Start the background sync service"""
        logger.info("Starting background sync service")

        # Sync all users every configured interval
        self.scheduler.add_job(
            self.sync_all_users,
            trigger=IntervalTrigger(minutes=settings.SYNC_USERS_INTERVAL_MINUTES),
            id="sync_all_users",
            name="Sync all users to cache"
        )

        # Sync all departments every configured interval
        self.scheduler.add_job(
            self.sync_all_departments,
            trigger=IntervalTrigger(minutes=settings.SYNC_DEPARTMENTS_INTERVAL_MINUTES),
            id="sync_all_departments",
            name="Sync all departments to cache"
        )

        # Clean expired cache entries every configured interval
        self.scheduler.add_job(
            self.clean_expired_cache,
            trigger=IntervalTrigger(minutes=settings.CACHE_CLEANUP_INTERVAL_MINUTES),
            id="clean_expired_cache",
            name="Clean expired cache entries"
        )

        self.scheduler.start()
        logger.info("Background sync service started successfully")

    def stop(self):
        """Stop the background sync service"""
        logger.info("Stopping background sync service")
        if self.scheduler.running:
            self.scheduler.shutdown(wait=True)
        logger.info("Background sync service stopped")

    async def sync_all_users(self):
        """Sync all users from DB to cache using delta caching"""
        db: Session = SessionLocal()
        try:
            logger.info("Starting delta user sync from DB to cache")

            now = datetime.now(timezone.utc)

            if self.last_sync_users is None:
                logger.info("First sync, doing full user sync")
                users = db.query(User).all()
                changed_users = users
                is_full_sync = True
            else:
                logger.info("Delta sync, getting users updated since %s", self.last_sync_users)
                users = db.query(User).filter(User.updated_at > self.last_sync_users).all()
                changed_users = users
                is_full_sync = False

            if not changed_users:
                logger.info("No changed users, skipping sync")
                return


            changed_users_data = [
                {
                    "user_id": str(user.user_id),
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": user.phone
                }
                for user in changed_users
            ]

            # Update individual user caches
            for user_data in changed_users_data:
                await CacheService.set_cached_user(user_data["user_id"], user_data, ttl=settings.CACHE_TTL_SECONDS)

            # Update the all_users list cache
            current_all_users = await CacheService.get_cached_all_users()
            if current_all_users is None:
                # If no cached list, fetch all and cache
                all_users = db.query(User).all()
                all_users_data = [
                    {
                        "user_id": str(user.user_id),
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "phone": user.phone
                    }
                    for user in all_users
                ]
                await CacheService.set_cached_all_users(all_users_data, ttl=settings.CACHE_TTL_SECONDS)
                logger.info("Set full all_users cache with %d users", len(all_users_data))
            else:
                updated_all_users = current_all_users.copy()
                changed_ids = {user["user_id"] for user in changed_users_data}
                
                updated_all_users = [u for u in updated_all_users if u["user_id"] not in changed_ids]
                
                updated_all_users.extend(changed_users_data)
                

                await CacheService.set_cached_all_users(updated_all_users, ttl=settings.CACHE_TTL_SECONDS)
                logger.info("Updated all_users cache with %d changed users", len(changed_users_data))

            self.last_sync_users = now
            logger.info("Delta synced %d users to cache", len(changed_users_data))

        except Exception as e:
            logger.error("Error syncing users: %s", e)
            raise
        finally:
            db.close()

    async def sync_all_departments(self):
        """Sync all departments from DB to cache using delta caching"""
        db: Session = SessionLocal()
        try:
            logger.info("Starting delta department sync from DB to cache")

            now = datetime.now(timezone.utc)

            if self.last_sync_departments is None:
                # First sync, do full sync
                logger.info("First sync, doing full department sync")
                departments = db.query(Department).all()
                changed_departments = departments
                is_full_sync = True
            else:
                # Delta sync: get departments updated since last sync
                logger.info("Delta sync, getting departments updated since %s", self.last_sync_departments)
                departments = db.query(Department).filter(Department.updated_at > self.last_sync_departments).all()
                changed_departments = departments
                is_full_sync = False

            if not changed_departments:
                logger.info("No changed departments, skipping sync")
                return

            # Convert changed departments to dict
            changed_departments_data = [
                {
                    "dept_id": str(department.dept_id),
                    "dept_name": department.dept_name
                }
                for department in changed_departments
            ]

            # Update individual department caches
            for dept_data in changed_departments_data:
                await CacheService.set_cached_department(dept_data["dept_id"], dept_data, ttl=settings.CACHE_TTL_SECONDS)

            # Update the all_departments list cache
            current_all_departments = await CacheService.get_cached_all_departments()
            if current_all_departments is None:
                # If no cached list, fetch all and cache
                all_departments = db.query(Department).all()
                all_departments_data = [
                    {
                        "dept_id": str(department.dept_id),
                        "dept_name": department.dept_name
                    }
                    for department in all_departments
                ]
                await CacheService.set_cached_all_departments(all_departments_data, ttl=settings.CACHE_TTL_SECONDS)
                logger.info("Set full all_departments cache with %d departments", len(all_departments_data))
            else:
                # Update the list with changed departments
                updated_all_departments = current_all_departments.copy()
                changed_ids = {dept["dept_id"] for dept in changed_departments_data}
                
                # Remove old entries for changed departments
                updated_all_departments = [d for d in updated_all_departments if d["dept_id"] not in changed_ids]
                
                # Add updated/new entries
                updated_all_departments.extend(changed_departments_data)
                
                await CacheService.set_cached_all_departments(updated_all_departments, ttl=settings.CACHE_TTL_SECONDS)
                logger.info("Updated all_departments cache with %d changed departments", len(changed_departments_data))

            self.last_sync_departments = now
            logger.info("Delta synced %d departments to cache", len(changed_departments_data))

        except Exception as e:
            logger.error("Error syncing departments: %s", e)
            raise
        finally:
            db.close()

    async def clean_expired_cache(self):
        """Clean expired cache entries (Redis handles TTL automatically, but we can add custom cleanup)"""
        try:
            logger.info("Cache cleanup check completed")
            # Redis automatically expires keys with TTL, but we can log or add custom logic
        except Exception as e:
            logger.error("Error during cache cleanup: %s", e)
            raise

    async def manual_invalidate_all_cache(self):
        """Manually invalidate all cache entries"""
        try:
            logger.info("Manually invalidating all cache entries")
            await CacheService.invalidate_user_cache()
            await CacheService.invalidate_department_cache()
            # Invalidate all user-department associations
            await CacheService.delete_pattern(f"{CacheService.USER_DEPARTMENT_PREFIX}*")
            logger.info("Manually invalidated all cache")
        except Exception as e:
            logger.error("Error invalidating cache: %s", e)
            raise


# Global instance
background_sync = BackgroundSyncService()