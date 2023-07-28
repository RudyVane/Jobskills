import os

from dotenv import load_dotenv
from flask import Flask
from .discord.flask import blueprint as discord_blueprint

# from .scrape import scrape


def main():
    load_dotenv()
    # as example of how to use the crawler:
    # scrape("https://www.yelgo.nl/vacatures/junior-developer-software/", print)

    app = Flask(__name__)
    app.config.from_prefixed_env()

    app.register_blueprint(discord_blueprint)

    @app.route("/")
    def hello():
        return "Hello World"

    if "API_KEY" in os.environ:
        from api_test.gpt import api_interaction

        @app.route("/test")
        def gpttest():
            skills_matrix_file = "./api_test/skills_matrix.txt"
            job_advert_file = "./api_test/job_advert.txt"
            result = api_interaction(skills_matrix_file, job_advert_file)
            return result

    # Todo:
    # -implement functionality in a proper format.
    # -decide file formats if any files are used
    """ 
    @app.route("/gpt")
    def gpt():
        skills_matrix_file = "userid/skils_matrix"
        job_advert_file = "url scraped"
        result = api_interaction(skills_matrix_file, job_advert_file)
        return result            
    """

    print(app.url_map)

    app.run(host="::", port=8080, debug=True)
