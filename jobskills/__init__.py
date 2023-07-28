from dotenv import load_dotenv
from flask import Flask
from .discord.flask import setup as discord_setup

def main():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_prefixed_env()

    @app.route("/")
    def hello():
        return "Hello World"

    discord_setup(app)

    print(app.url_map)

    app.run(host="app", port=8080, debug=True)