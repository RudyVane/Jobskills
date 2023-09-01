import os

from flask.blueprints import Blueprint, BlueprintSetupState

from flask_discord_interactions import DiscordInteractions
from .commands import blueprints

blueprint = Blueprint("discord_integration", __name__)


def _setup(state: BlueprintSetupState):
    discord = DiscordInteractions(state.app)

    for bp in blueprints:
        discord.register_blueprint(bp)

    discord.set_route("/interaction/")

    # TODO: move to option in state.settings
    if "TESTING_GUILD" in os.environ:
        discord.update_commands(guild_id=os.environ["TESTING_GUILD"])
    else:
        state.app.logger.warn(
            "Not updating discord commands, no 'TESTING_GUILD' id set"
        )


def dump_commands():
    return [
        command.dump() for bp in blueprints for command in bp.discord_commands.values()
    ]


blueprint.record_once(_setup)
