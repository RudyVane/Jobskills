from arq import create_pool
from quart import g

from jobskills.config import settings


async def get_queue():
    if "queue" not in g:
        g.queue = await create_pool(settings.redis)
    return g.queue


def setup(app):
    """
    Wrap teardown to avoid a circular dependency
    """
    @app.teardown_appcontext
    async def teardown_queue(_e):
        queue = g.pop("queue", None)
        if queue is not None:
            await queue.close()
