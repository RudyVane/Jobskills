import os

from flask import Flask
from flask_discord_interactions import DiscordInteractions

from .commands import blueprints

def setup(app: Flask):
    discord = DiscordInteractions(app)

    for bp in blueprints:
        discord.register_blueprint(bp)

    discord.set_route("/interaction/")

    if "TESTING_GUILD" in os.environ:
        discord.update_commands(guild_id=os.environ["TESTING_GUILD"])
    else:
        app.logger.warn("Not updating discord commands, no 'TESTING_GUILD' id set")
