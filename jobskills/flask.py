import os
from pathlib import Path

import quart.flask_patch  # noqa: F401
from asgiref.wsgi import WsgiToAsgi
from quart import Quart

from .discord.flask import blueprint as discord_blueprint

app = Quart(__name__)
app.config.from_prefixed_env(prefix="FLASK")

# FIXME: extract to common method
app.config.update(
    {
        key.removesuffix("_FILE"): Path(app.config[key]).read_text()
        for (key, value) in app.config.items()
        if key.endswith("_FILE")
    }
)

app.register_blueprint(discord_blueprint)


@app.route("/")
def hello():
    return "Hello World"


if "API_KEY" in os.environ:
    from .gpt import api_interaction

    @app.route("/test")
    def gpttest():
        skills_matrix_file = "./api_test/skills_matrix.txt"
        job_advert_file = "./api_test/job_advert.txt"
        result = api_interaction(skills_matrix_file, job_advert_file)
        return result


asgi_app = WsgiToAsgi(app)
