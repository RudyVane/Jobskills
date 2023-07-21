import os

from flask import Flask
from dotenv import load_dotenv
from flask_discord_interactions import DiscordInteractions

app = Flask(__name__)
discord = DiscordInteractions(app)

@app.route("/")
def hello():
    return "Hello World"

@discord.command()
def ping(ctx):
    return "Pong!"


if __name__ == '__main__':
    print(app.url_map)

    load_dotenv()
    app.config.from_prefixed_env()
    
    discord.set_route("/interaction/")
    discord.update_commands(guild_id=os.environ["TESTING_GUILD"])

    app.run(host="app", port=8080, debug=True)