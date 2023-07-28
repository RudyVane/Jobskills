from flask_discord_interactions import DiscordInteractionsBlueprint


bp = DiscordInteractionsBlueprint()

@bp.command()
def ping(ctx):
    return "Pong!"