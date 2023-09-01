import os

from pathlib import Path
from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from .discord.flask import blueprint as discord_blueprint

app = Flask(__name__)
app.config.from_prefixed_env()
for key in app.config.keys():
    # FIXME: created common utility to do this
    new_key = key.removesuffix("_FILE")
    if new_key != key:
        app.config[new_key] = Path(app.config[key]).read_text()

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
