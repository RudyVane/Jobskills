from flask import Flask
from discord.interaction import discord_interaction

app = Flask(__name__)

app.register_blueprint(discord_interaction, url_prefix='/interaction')

@app.route("/")
def hello():
    return "Hello World"


if __name__ == '__main__':
    print(app.url_map)
    app.run(host="app", port=8080, debug=True)