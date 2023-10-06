from dotenv import load_dotenv


def main():
    load_dotenv()

    from .flask import app

    app.run(host="::", port=8080, debug=True)
