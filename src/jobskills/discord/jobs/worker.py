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


# should determine the file type. attempt to parse it?, before GPT gets called.
async def scrape_pipeline(arq_ctx, dc_ctx, url: str, file: any):
    print("scrape_pipelines started")
    async with get_queue() as q:
        # enqueue file parsing.
        file_parsing_job = await q.enqueue_job("fileparser_handler", file)
        file_content = await file_parsing_job.result()

        # Check if the file type is unsupported
        if file_content == "Unsupported filetype":
            # Handle the error (e.g., send a message to the user or cancel the pipeline)
            await q.enqueue_job(
                "send_to_discord",
                dc_ctx,
                "Unsupported file type provided. Please upload a supported format.",
            )
            return

        # enqueue scraping
        scrape_job = await q.enqueue_job("scrape_handler", url)
        scrape_res = await scrape_job.result()
        logger.debug(scrape_res)

        # enqueue gpt
        gpt_result = await q.enqueue_job("gpt_handler", scrape_res, file_content)

        # send result back
        await q.enqueue_job("send_to_discord", dc_ctx, gpt_result)


async def send_to_discord(arq_ctx, dc_ctx, msg: str):
    try:
        dc_ctx.edit(Message(content=msg))
    except HTTPError as e:
        logger.debug(
            "REQUEST\nurl: {}\nbody: {}\nheaders: {}".format(
                e.request.url, e.request.body, e.request.headers
            )
        )
        logger.debug("RESPONSE\n{}".format(e.response.json))


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
        logger.debug(
            "REQUEST\nurl: {}\nbody: {}\nheaders: {}".format(
                e.request.url, e.request.body, e.request.headers
            )
        )
        logger.debug("RESPONSE\n{}".format(e.response.json))
    # print(msg)


class WorkerSettings:
    functions = [scrape_pipeline, scrape_handler, message_edit]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(settings.redis.dsn)
