# ruff: noqa: E501

from flask_discord_interactions import DiscordInteractionsBlueprint, Message

bp = DiscordInteractionsBlueprint()


@bp.command()
def help(ctx):
    return Message(
        content="""Welcome to the jobskills-matcher

This app is ment to compare your own skills with the required skills from a job offer text.

To start this app type; /1

The pop-up will ask you to paste your resume or your skillmatrix

Then you give the URL of the job offer

By clicking the OK button the app will compare both inputs and return a list of matching skills 
and a matching percentage.""",
        ephemeral=True,
    )
