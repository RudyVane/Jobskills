import os

from flask import Flask
from flask_discord_interactions import DiscordInteractions, Attachment, Message


def setup(app: Flask):
    discord = DiscordInteractions(app)

    # TODO: split off commands with DiscordInteractionBlueprint

    @discord.command()
    def ping(ctx):
        return "Pong!"

    @discord.command()
    def offer(ctx, item: Attachment):
        return Message(
            content="thanks!",
            ephemeral=True
        )

    discord.set_route("/interaction/")
    
    if "TESTING_GUILD" in os.environ:
        discord.update_commands(guild_id=os.environ["TESTING_GUILD"])
    else:
        app.logger.warn("Not updating discord commands, no 'TESTING_GUILD' id set")