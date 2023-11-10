from io import StringIO

from arq.connections import RedisSettings
from arq.jobs import ResultNotFound, logger
from flask_discord_interactions import Message
from requests import HTTPError

from jobskills.config import settings
from jobskills.jobqueue import get_queue


async def startup(ctx):
    pass


async def shutdown(ctx):
    pass


async def scrape_pipeline(arq_ctx, dc_ctx, url: str):
    print("scrape_pipelines started")
    async with get_queue() as q:
        scrape_job = await q.enqueue_job("scrape_handler", url)
        scrape_res = await scrape_job.result()
        logger.debug(scrape_res)
        await q.enqueue_job("message_edit", dc_ctx, scrape_res)


async def scrape_handler(arq_ctx, url: str):
    async with get_queue() as q:
        scrape_job = await q.enqueue_job("scrape", url, _queue_name="arq:scraper")
        try:
            scrape_res = await scrape_job.result()
            return str(scrape_res.get("text", "Failed to scrape!"))
        except TimeoutError:
            return "No result yet!"
        except ResultNotFound:
            return "Failed to scrape!"


async def message_edit(arq_ctx, dc_ctx, msg: str):
    try:
        if len(msg) < settings.discord.msg_max_len:
            dc_ctx.edit(Message(content=msg))
        else:
            with StringIO(msg) as buff:
                dc_ctx.edit(Message(file=("message.txt", buff, "text/plain")))
    except HTTPError as e:
        logger.debug(
            "REQUEST\nurl: {}\nbody: {}\nheaders: {}".format(
                e.request.url, e.request.body, e.request.headers
            )
        )
        logger.debug("RESPONSE\n{}".format(e.response.json))
        dc_ctx.edit(
            Message(
                content="Error {}: {}".format(e.response.status_code, e.response.reason)
            )
        )


class WorkerSettings:
    functions = [scrape_pipeline, scrape_handler, message_edit]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(settings.redis.dsn)
