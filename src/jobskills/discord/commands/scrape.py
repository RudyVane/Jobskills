from flask_discord_interactions import DiscordInteractionsBlueprint, Message

from jobskills.jobqueue import get_queue

bp = DiscordInteractionsBlueprint()

# TODO allow file upload with url. modal i guess?
@bp.command()
async def scrape(ctx, url: str, file: any):
    async with get_queue() as q:
        await q.enqueue_job("scrape_pipeline", ctx.freeze(), url, file)
    return Message(deferred=True)
