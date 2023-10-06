from flask_discord_interactions import (
    ActionRow,
    DiscordInteractionsBlueprint,
    Modal,
    TextInput,
    TextStyles,
    FileInput,
    Message
)

from jobskills.jobqueue import get_queue

bp = DiscordInteractionsBlueprint()

# TODO allow file upload with url. modal i guess?
@bp.command()
def scrape(ctx):
    # Define the modal fields
    fields = [
        ActionRow(
            [
                TextInput("url_input", "Enter the URL:", required=True),
                FileInput("file_input", "Upload resume:", required=True)
            ]
        )
    ]
    # Open the modal
    return Modal("scrape_modal", "Scrape Data", fields)

@bp.custom_handler("scrape_modal")
async def scrape_submit(ctx):
    # Retrieve data from the modal
    url = ctx.get_component("url_input").value
    file = ctx.get_component("file_input").value

    # Enqueue the scrape_pipeline job with the provided data
    async with get_queue() as q:
        await q.enqueue_job("scrape_pipeline", ctx.freeze(), url, file)
    return Message(content="Processing your request...")
