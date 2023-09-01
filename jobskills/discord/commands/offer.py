from flask_discord_interactions import Attachment, DiscordInteractionsBlueprint, Message

bp = DiscordInteractionsBlueprint()


@bp.command()
def offer(ctx, item: Attachment):
    return Message(content="thanks!", ephemeral=True)
