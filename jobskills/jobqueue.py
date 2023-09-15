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

    q = await create_pool(get_redis_settings())
    try:
        yield q
    finally:
        await q.close()


def get_redis_settings():
    """
    Temporary centralized Redis settings until proper config management
    """
    if "REDIS_DSN" in environ:
        return RedisSettings.from_dsn(environ.get("REDIS_DSN"))
    else:
        return RedisSettings()
