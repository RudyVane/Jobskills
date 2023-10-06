import os

from dynaconf import FlaskDynaconf
from flask_discord_interactions import DiscordInteractions
from quart import Quart
from quart.blueprints import Blueprint, BlueprintSetupState

from ..config import settings


def _setup(state: BlueprintSetupState):
    from .commands import blueprints

    discord = DiscordInteractions(state.app)

    for bp in blueprints:
        discord.register_blueprint(bp)

    discord.set_route_async("/interaction/")

    # TODO: move to option in state.settings
    if "TESTING_GUILD" in os.environ:
        discord.update_commands(guild_id=os.environ["TESTING_GUILD"])
    else:
        state.app.logger.warning(
            "Not updating discord commands, no 'TESTING_GUILD' id set"
        )


blueprint = Blueprint("discord_integration", __name__)
blueprint.record_once(_setup)


def discord_extension(app):
    app.register_blueprint(blueprint)


def make_app():
    app = Quart(__name__)

    FlaskDynaconf(app, dynaconf_instance=settings, extensions_list="EXTENSIONS")

    @app.route("/")
    def hello():
        return "Hello World"

    if "API_KEY" in os.environ:
        from ..gpt import api_interaction

        @app.route("/test")
        def gpttest():
            skills_matrix_file = "./api_test/skills_matrix.txt"
            job_advert_file = "./api_test/job_advert.txt"
            result = api_interaction(skills_matrix_file, job_advert_file)
            return result

    return app
