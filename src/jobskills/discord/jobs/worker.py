from io import StringIO

from arq import create_pool
from arq.jobs import ResultNotFound, logger
from flask_discord_interactions import Message
from requests import HTTPError

from jobskills.config import settings


async def startup(ctx):
    ctx["pool"] = await create_pool(settings.redis)


async def shutdown(ctx):
    await ctx["pool"].close()


async def scrape_pipeline(arq_ctx, dc_ctx, url: str):
    print("scrape_pipelines started")

    scrape_job = await arq_ctx["pool"].enqueue_job("scrape_handler", url)
    scrape_res = await scrape_job.result()
    logger.debug(scrape_res)
    await arq_ctx["pool"].enqueue_job("message_edit", dc_ctx, scrape_res)


async def scrape_handler(arq_ctx, url: str):
    scrape_job = await arq_ctx["pool"].enqueue_job(
        "scrape", url, _queue_name="arq:scraper"
    )
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
            await dc_ctx.edit(Message(content=msg))
        else:
            with StringIO(msg) as buff:
                await dc_ctx.edit(Message(file=("message.txt", buff, "text/plain")))
    except HTTPError as e:
        await dc_ctx.edit(
            Message(
                content="Error {}: {}".format(e.response.status_code, e.response.reason)
            )
        )


class WorkerSettings:
    functions = [scrape_pipeline, scrape_handler, message_edit]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = settings.redis
