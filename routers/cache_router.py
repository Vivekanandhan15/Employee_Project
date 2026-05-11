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
    Requires admin privileges.
    """
    # TODO: Add admin check here
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

    await background_sync.manual_invalidate_all_cache()

    return {"message": "All cache entries invalidated successfully"}