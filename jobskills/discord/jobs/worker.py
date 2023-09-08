import quart.flask_patch  # noqa: F401
from arq.jobs import ResultNotFound, logger
from flask_discord_interactions import Message
from requests import HTTPError

from jobskills.jobqueue import get_queue, get_redis_settings


async def startup(ctx):
    pass


async def shutdown(ctx):
    pass


async def scrape_pipeline(arq_ctx, dc_ctx, url: str):
    print("scrape_pipelines started")
    async with get_queue() as q:
        # await q.enqueue_job(
        #     "message_edit", dc_ctx, "Scraping...", {}
        # )  # , _job_id=("edit_step1:{}{}".format(dc_ctx.guild_id, url)))
        scrape_job = await q.enqueue_job(
            "scrape_handler", url
        )  # , _job_id=("scrape_handler:{}{}".format(dc_ctx.guild_id, url)))
        scrape_res = await scrape_job.result()
        logger.debug(scrape_res)
        await q.enqueue_job(
            "message_edit", dc_ctx, scrape_res
        )  # , _job_id=("edit_step2:{}{}".format(dc_ctx.guild_id, url)))


async def scrape_handler(arq_ctx, url: str):
    async with get_queue() as q:
        scrape_job = await q.enqueue_job(
            "scrape", url, _queue_name="arq:scraper"
        )  # , _job_id=("scrape:{}{}".format(dc_ctx.guild_id, url)))
        try:
            scrape_res = await scrape_job.result()
            return str(scrape_res.get("text", "Failed to scrape!"))
        except TimeoutError:
            return "No result yet!"
        except ResultNotFound:
            return "Failed to scrape!"


async def message_edit(arq_ctx, dc_ctx, msg: str):
    try:
        dc_ctx.edit(Message(content=msg))
    except HTTPError as e:
        logger.debug(e.request)
        logger.debug(e.response)
    # print(msg)


class WorkerSettings:
    functions = [scrape_pipeline, scrape_handler, message_edit]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = get_redis_settings()
