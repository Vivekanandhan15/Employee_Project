from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_dependency import get_current_user
from services.background_sync_service import background_sync

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