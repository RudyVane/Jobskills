from dotenv import load_dotenv


def main():
    load_dotenv()
    # as example of how to use the crawler:
    # scrape("https://www.yelgo.nl/vacatures/junior-developer-software/", print)

    from .flask import app

    app.run(host="::", port=8080, debug=True)
