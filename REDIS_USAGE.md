# Redis Usage in This Project

This document explains how Redis is used in this FastAPI project, which libraries are involved, the caching design, and the key code paths. It is written for beginners and for explaining the system in meetings.

## 1. What is Redis?

- Redis is an in-memory data store used for fast access to data.
- It is often used as a cache to store frequently read data and reduce database load.
- In this project, Redis is used to cache user, department, and user-department association data.

## 2. Why use Redis here?

- The application reads user lists, user details, department lists, and user-department relationships.
- Reading from PostgreSQL/SQLAlchemy every time is slower than reading from Redis.
- Redis reduces latency and improves performance for repeated requests.
- Cached data is stored temporarily with a TTL (time-to-live).

## 3. Libraries used

- `redis` (Redis Python client)
  - The project uses the asynchronous Redis client via `redis.asyncio`.
- `json`
  - Data is serialized to JSON strings before saving in Redis.
  - Data is deserialized back into Python objects when reading.
- `apscheduler`
  - Used for background sync jobs if the application wants to refresh cache periodically.

## 4. Redis connection setup

The Redis connection is configured in `database/redis.py`:

```python
import os
from redis import asyncio as redis

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    decode_responses=True
)
```

- `REDIS_HOST` and `REDIS_PORT` are environment variables.
- `decode_responses=True` makes Redis return strings instead of bytes.

## 5. Cache service layer

The main Redis logic is in `services/cache_service.py`.

### Core functions

- `get_cache(key)`
  - Reads a Redis key and returns parsed JSON data.
- `set_cache(key, value, ttl=300)`
  - Writes data to Redis with a TTL (default 300 seconds).
- `delete_cache(key)`
  - Deletes a key from Redis.
- `delete_pattern(pattern)`
  - Deletes all keys that match a Redis pattern.

### Data-specific helpers

The service defines key prefixes and helpers for:

- Users
  - `user:<user_id>`
  - `all_users`
- Departments
  - `department:<dept_id>`
  - `all_departments`
- User-department associations
  - `user_department:user:<user_id>`
  - `user_department:department:<dept_id>`
  - `user_department:<user_id>:<dept_id>`

These helper functions simplify getting, setting, and invalidating cached objects.

### Example of `get_cache` and `set_cache`

```python
@staticmethod
async def get_cache(key: str) -> Optional[Any]:
    data = await redis_client.get(key)
    if data:
        return json.loads(data)
    return None

@staticmethod
async def set_cache(key: str, value: Any, ttl: int = 300) -> None:
    await redis_client.set(key, json.dumps(value), ex=ttl)
```

## 6. How caching is used in services

### User service

In `services/user_service.py`:

- `get_all_users` first checks Redis with `CacheService.get_cached_all_users()`.
- If the cache exists, it returns cached data and avoids the database.
- If not, it reads from the database, converts rows to dictionaries, stores the result in Redis with `CacheService.set_cached_all_users(users_data)`, and returns it.

Example flow:

1. Request to get all users.
2. Check Redis key `all_users`.
3. If found, return cached users.
4. If missing, query DB, cache result, return users.

- `get_user_by_id` uses the same pattern for a single user via `user:<user_id>`.

### Cache invalidation

When user data changes, the cache is invalidated:

- `create_user`, `update_user`, and `delete_user` call `CacheService.invalidate_user_cache(user_id)`.
- This removes both the individual user cache and the cached list of all users.

That ensures stale data is not served after changes.

### User-department service

In `services/user_department_service.py`:

- `get_user_departments(user_id)` checks `user_department:user:<user_id>` before querying the DB.
- `get_department_users(dept_id)` checks `user_department:department:<dept_id>`.

When relationships change:

- `assign_users_departments` invalidates relevant user/department caches.
- `remove_user_from_department` invalidates the specific association cache.

## 7. Background sync and manual cache control

### Background sync

`services/background_sync_service.py` contains jobs that can refresh cache automatically.

- `sync_all_users()` writes all users from the DB into Redis.
- `sync_all_departments()` writes all departments into Redis.
- `clean_expired_cache()` is present for monitoring, although Redis automatically removes expired keys.

This is useful when you want the cache to be refreshed regularly.

### Manual admin endpoints

`routers/cache_router.py` exposes admin endpoints:

- `POST /cache/invalidate-all`
  - Manually clears all caches.
- `POST /cache/sync-all`
  - Forces a sync of all users and departments from DB to Redis.

These endpoints are protected by an admin check.

## 8. Key Redis concepts for beginners

- Cache key: a unique name used to store a value in Redis.
- TTL (`ex` argument): controls how long Redis keeps a key before expiring it.
- Cache hit: when Redis returns data and the application does not need the database.
- Cache miss: when Redis has no data, so the application loads from the database and caches it.
- Invalidation: removing or updating cached data after the source data changes.

## 9. Important patterns in this code

- `Cache first, DB fallback`:
  - Try Redis first, if missing then query the database.
- `Serialize before cache`:
  - Convert Python objects to JSON strings before storing.
- `Invalidate stale cache`:
  - Remove old cache entries after writes or relationship changes.
- `Use prefixes`:
  - Group related keys using prefixes such as `user:` and `department:`.

## 10. Example Redis key usage in this project

- `all_users` -> JSON list of all users.
- `user:123` -> JSON object for user with ID `123`.
- `all_departments` -> JSON list of all departments.
- `department:45` -> JSON object for department with ID `45`.
- `user_department:user:123` -> departments for user `123`.
- `user_department:department:45` -> users for department `45`.

## 11. Full endpoint example: `GET /users/{user_id}`

This is a complete flow for the API endpoint in `routers/user_router.py`:

- Route: `GET /users/{user_id}`
- Handler: `get_user_by_id`
- Service: `UserService.get_user_by_id`
- Cache key: `user:<user_id>`

### Step-by-step flow

1. The client requests `GET /users/123`.
2. FastAPI calls `routers/user_router.py` `get_user_by_id` function.
3. That function depends on `get_db()` and `get_current_user()` and then calls `UserService.get_user_by_id(user_id, db)`.
4. In `services/user_service.py`, the method first checks Redis:

```python
cached_user = await CacheService.get_cached_user(user_id)
if cached_user:
    return cached_user
```

5. If Redis has `user:123`, that is a cache hit: the API returns the cached JSON and the database is not queried.
6. If Redis does not have it (cache miss), the service loads user data from the database:

```python
user = db.query(User).filter(User.user_id == user_id).first()
```

7. The service converts the SQLAlchemy object into a plain dictionary.
8. It stores the result in Redis using `CacheService.set_cached_user(user_id, user_data)`.
9. Redis saves the data under `user:123` as a JSON string, with a TTL of 300 seconds.
10. The API returns the user data to the client.

### What Redis is doing here

- Redis is the first place the code looks for data.
- If the user is cached, the response is much faster.
- If not cached, Redis is updated after the DB read.
- The cache entry expires automatically after 5 minutes.

### What happens after data changes

If the same user is updated or deleted, the cache is invalidated in `UserService.update_user` and `UserService.delete_user` using:

```python
asyncio.create_task(CacheService.invalidate_user_cache(user_id))
```

This removes:

- `user:<user_id>`
- `all_users`

That ensures the next `GET /users/{user_id}` request reads fresh data from the database and refreshes the cache.

## 12. How to explain this in a meeting

- Start with: "Redis is used as a fast cache layer for read-heavy endpoints."
- Mention that the app still uses the database for writes and when cache misses occur.
- Explain that Redis stores JSON values with keys like `user:123` and automatically expires them after 5 minutes.
- Point out that the cache service centralizes Redis usage, so services do not talk to Redis directly.
- Note the invalidation steps: whenever user or department data changes, the related cache is cleared.

## 13. Summary

This project uses Redis as a caching layer to make user and department read operations faster.
The main Redis work is handled by `services/cache_service.py`, with connection setup in `database/redis.py`.
The application uses cache lookups first, then falls back to the database, and invalidates cache after writes.

This design is easy to explain to beginners and shows a standard cache pattern used in many web APIs.
