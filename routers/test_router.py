from fastapi import APIRouter

from database.redis import redis_client

router = APIRouter()


@router.get('/redis-test')
async def redis_test():

    await redis_client.set("message", "Redis Working")

    value = await redis_client.get("message")

    return {"redis":value}