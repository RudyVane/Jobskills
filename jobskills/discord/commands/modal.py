from flask_discord_interactions import DiscordInteractionsBlueprint, Modal, ActionRow, TextInput, TextStyles


bp = DiscordInteractionsBlueprint()

@bp.command()
def modal_test(ctx):
    fields = [
        ActionRow([
            TextInput("test_input", "What do you have to say?", style=TextStyles.PARAGRAPH)
        ])
    ]
    return Modal("modal_test_response", "Hi There", fields)

@bp.custom_handler("modal_test_response")
def modal_test_response(ctx):
    input = ctx.get_component("test_input")
    return f"You told me about {len(input.value)} characters of input"