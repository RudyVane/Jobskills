from contextlib import asynccontextmanager
from os import environ

from arq import create_pool
from arq.connections import RedisSettings


# TODO: use a centralized config manager
@asynccontextmanager
async def get_queue():
    """
    Create a job queue for current context. Usage:
    async with get_queue() as q:
        await q.enqueue_job(...)
    """

    redisSettings = RedisSettings()

    if "REDIS_DSN" in environ:
        redisSettings = RedisSettings.from_dsn(environ.get("REDIS_DSN"))

    q = await create_pool(redisSettings)
    try:
        yield q
    finally:
        await q.close()
