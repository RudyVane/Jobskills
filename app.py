from flask import Flask
from discord.interaction import discord_interaction

app = Flask(__name__)

app.register_blueprint(discord_interaction, url_prefix='/interaction')

@app.route("/")
def hello():
    return "Hello World"


if __name__ == '__main__':
    print(app.url_map)
    app.config.update(
        DISCORD_PUBLIC_KEY="ada8547aa7193a4b570c7bed1b13d523a07b5a20139a57753f7715b21c3d9b1f"
    )
    app.run(host="app", port=8080, debug=True)