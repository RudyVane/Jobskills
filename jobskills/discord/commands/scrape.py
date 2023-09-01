from flask_discord_interactions import DiscordInteractionsBlueprint, Message
from jobskills.jobqueue import get_queue

bp = DiscordInteractionsBlueprint()

@bp.command()
async def scrape(ctx, url: str):
    async with get_queue() as q:
        await q.enqueue_job("scrape_pipeline", ctx.freeze(), url)
    return Message(deferred=True)
