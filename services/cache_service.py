import json
import asyncio
from typing import Any, Optional, List
from database.redis import redis_client

class CacheService:
    # Cache key prefixes
    USER_PREFIX = "user:"
    DEPARTMENT_PREFIX = "department:"
    USER_DEPARTMENT_PREFIX = "user_department:"
    ALL_USERS_KEY = "all_users"
    ALL_DEPARTMENTS_KEY = "all_departments"

    @staticmethod
    async def get_cache(key: str) -> Optional[Any]:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    @staticmethod
    async def set_cache(key: str, value: Any, ttl: int = 300) -> None:
        await redis_client.set(key, json.dumps(value), ex=ttl)

    @staticmethod
    async def delete_cache(key: str) -> None:
        await redis_client.delete(key)

    @staticmethod
    async def delete_pattern(pattern: str) -> None:
        """Delete all keys matching a pattern"""
        keys = await redis_client.keys(pattern)
        if keys:
            await redis_client.delete(*keys)

    @staticmethod
    async def invalidate_user_cache(user_id: str = None) -> None:
        """Invalidate user-related cache"""
        if user_id:
            await CacheService.delete_cache(f"{CacheService.USER_PREFIX}{user_id}")
            await CacheService.delete_pattern(f"{CacheService.USER_DEPARTMENT_PREFIX}user:{user_id}:*")
        await CacheService.delete_cache(CacheService.ALL_USERS_KEY)

    @staticmethod
    async def invalidate_department_cache(dept_id: str = None) -> None:
        """Invalidate department-related cache"""
        if dept_id:
            await CacheService.delete_cache(f"{CacheService.DEPARTMENT_PREFIX}{dept_id}")
            await CacheService.delete_pattern(f"{CacheService.USER_DEPARTMENT_PREFIX}department:{dept_id}:*")
        await CacheService.delete_cache(CacheService.ALL_DEPARTMENTS_KEY)

    @staticmethod
    async def invalidate_user_department_cache(user_id: str = None, dept_id: str = None) -> None:
        """Invalidate user-department association cache"""
        if user_id:
            await CacheService.delete_cache(f"{CacheService.USER_DEPARTMENT_PREFIX}user:{user_id}")
        if dept_id:
            await CacheService.delete_cache(f"{CacheService.USER_DEPARTMENT_PREFIX}department:{dept_id}")
        if user_id and dept_id:
            await CacheService.delete_cache(f"{CacheService.USER_DEPARTMENT_PREFIX}{user_id}:{dept_id}")

    @staticmethod
    async def get_cached_user(user_id: str) -> Optional[dict]:
        return await CacheService.get_cache(f"{CacheService.USER_PREFIX}{user_id}")

    @staticmethod
    async def set_cached_user(user_id: str, user_data: dict, ttl: int = 300) -> None:
        await CacheService.set_cache(f"{CacheService.USER_PREFIX}{user_id}", user_data, ttl)

    @staticmethod
    async def get_cached_all_users() -> Optional[List[dict]]:
        # Try to get from the list cache first
        cached_list = await CacheService.get_cache(CacheService.ALL_USERS_KEY)
        if cached_list:
            return cached_list
        
        # If not, reconstruct from individual user caches
        # This is for delta caching fallback
        # But for now, keep as is
        return None

    @staticmethod
    async def set_cached_all_users(users: List[dict], ttl: int = 300) -> None:
        await CacheService.set_cache(CacheService.ALL_USERS_KEY, users, ttl)

    @staticmethod
    async def set_cached_all_users_delta(users: List[dict], ttl: int = 300) -> None:
        """Set all users individually for delta caching"""
        # Set individual user caches
        for user in users:
            await CacheService.set_cached_user(user["user_id"], user, ttl)
        
        # Also set the list cache
        await CacheService.set_cache(CacheService.ALL_USERS_KEY, users, ttl)

    @staticmethod
    async def get_cached_department(dept_id: str) -> Optional[dict]:
        return await CacheService.get_cache(f"{CacheService.DEPARTMENT_PREFIX}{dept_id}")

    @staticmethod
    async def set_cached_department(dept_id: str, dept_data: dict, ttl: int = 300) -> None:
        await CacheService.set_cache(f"{CacheService.DEPARTMENT_PREFIX}{dept_id}", dept_data, ttl)

    @staticmethod
    async def get_cached_all_departments() -> Optional[List[dict]]:
        return await CacheService.get_cache(CacheService.ALL_DEPARTMENTS_KEY)

    @staticmethod
    async def set_cached_all_departments(departments: List[dict], ttl: int = 300) -> None:
        await CacheService.set_cache(CacheService.ALL_DEPARTMENTS_KEY, departments, ttl)

    @staticmethod
    async def get_cached_user_departments(user_id: str) -> Optional[dict]:
        return await CacheService.get_cache(f"{CacheService.USER_DEPARTMENT_PREFIX}user:{user_id}")

    @staticmethod
    async def set_cached_user_departments(user_id: str, data: dict, ttl: int = 300) -> None:
        await CacheService.set_cache(f"{CacheService.USER_DEPARTMENT_PREFIX}user:{user_id}", data, ttl)

    @staticmethod
    async def get_cached_department_users(dept_id: str) -> Optional[dict]:
        return await CacheService.get_cache(f"{CacheService.USER_DEPARTMENT_PREFIX}department:{dept_id}")

    @staticmethod
    async def set_cached_department_users(dept_id: str, data: dict, ttl: int = 300) -> None:
        await CacheService.set_cache(f"{CacheService.USER_DEPARTMENT_PREFIX}department:{dept_id}", data, ttl)

# Backward compatibility
async def get_cache(key: str):
    return await CacheService.get_cache(key)

async def set_cache(key: str, value, ttl=300):
    await CacheService.set_cache(key, value, ttl)

async def delete_cache(key: str):
    await CacheService.delete_cache(key)