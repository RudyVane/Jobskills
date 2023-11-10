from flask_discord_interactions import DiscordInteractionsBlueprint, Message

from jobskills.discord.jobqueue import get_queue

bp = DiscordInteractionsBlueprint()


@bp.command()
async def scrape(ctx, url: str):
    queue = await get_queue()
    await queue.enqueue_job("scrape_pipeline", ctx.freeze(), url)
    return Message(deferred=True, ephemeral=True)
