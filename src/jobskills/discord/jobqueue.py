from arq import create_pool
from quart import g

from jobskills.config import settings
from jobskills.flask import asgi_app as app


async def get_queue():
    if "queue" not in g:
        g.queue = await create_pool(settings.redis)
    return g.queue


@app.teardown_appcontext
async def teardown_queue(_e):
    queue = g.pop("queue", None)
    if queue is not None:
        await queue.close()
