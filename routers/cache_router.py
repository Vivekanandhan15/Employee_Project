from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_dependency import get_current_user
from services.background_sync_service import background_sync
from database.redis import redis_client
from services.cache_service import CacheService

router = APIRouter(
    prefix="/cache",
    tags=["Cache Management"]
)


@router.post("/invalidate-all")
async def invalidate_all_cache(current_user: dict = Depends(get_current_user)):
    """
    Manually invalidate all cache entries.
    """
    await background_sync.manual_invalidate_all_cache()

    return {"message": "All cache entries invalidated successfully"}


@router.post("/sync-all")
async def sync_all_data(current_user: dict = Depends(get_current_user)):
    """
    Manually trigger sync of all data from DB to cache.
    """

    try:
        await background_sync.sync_all_users()
        await background_sync.sync_all_departments()
        return {"message": "Data sync completed successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sync failed: {str(e)}"
        )

@router.get("/status")
async def cache_status(current_user: dict = Depends(get_current_user)):
    """
    Get current cache status - shows what's stored in Redis.
    """
    try:
        all_users = await CacheService.get_cached_all_users()
        all_departments = await CacheService.get_cached_all_departments()
        
        # Get count of individual user keys
        user_keys = await redis_client.keys("user:*")
        dept_keys = await redis_client.keys("department:*")
        
        return {
            "redis_connection": "OK",
            "all_users_cached": all_users is not None,
            "all_users_count": len(all_users) if all_users else 0,
            "all_departments_cached": all_departments is not None,
            "all_departments_count": len(all_departments) if all_departments else 0,
            "individual_user_keys": len(user_keys) if user_keys else 0,
            "individual_department_keys": len(dept_keys) if dept_keys else 0,
            "data": {
                "all_users": all_users,
                "all_departments": all_departments
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cache status check failed: {str(e)}"
        )
