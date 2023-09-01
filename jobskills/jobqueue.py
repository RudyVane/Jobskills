from contextlib import asynccontextmanager

from arq import create_pool
from arq.connections import RedisSettings


@asynccontextmanager
async def get_queue():
    """
    Create a job queue for current context. Usage:
    async with get_queue() as q:
        await q.enqueue_job(...)
    """
    q = await create_pool(RedisSettings())
    try:
        yield q
    finally:
        await q.close()
