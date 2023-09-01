import os

from dotenv import load_dotenv
from flask import Flask
from .discord.flask import blueprint as discord_blueprint

# from .scrape import scrape


def main():
    load_dotenv()
    # as example of how to use the crawler:
    # scrape("https://www.yelgo.nl/vacatures/junior-developer-software/", print)

    from .flask import app

    app.run(host="::", port=8080, debug=True)