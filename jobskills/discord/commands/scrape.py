from flask_discord_interactions import DiscordInteractionsBlueprint, Message
from arq import create_pool
from arq.connections import RedisSettings

bp = DiscordInteractionsBlueprint()

queue = create_pool(RedisSettings())

# def _callback(ctx, item: dict):
#     ctx.edit(Message(content=str(item)))

@bp.command()
async def scrape(ctx, url: str):
    def _callback(item: dict):
        ctx.edit(Message(content=str(item)))
    await queue.enqueue_job("scrape",
                      url,                                          # url to scrape
                      _job_id=("{}{}".format(ctx.guild_id, url)),   # set job ID to avoid queueing multiple scrapes of the same url
                      cb=_callback)                                 # callback to edit message with 
    return Message(deferred=True)
