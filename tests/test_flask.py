import jobskills.discord.flask  # noqa: F401


def test_flask_patch():
    from flask import request

    assert "quart_flask_patch" in type(request).__module__


def test_async_works():
    from flask_discord_interactions import DiscordInteractions
    from quart import Quart

    DiscordInteractions().set_route_async("/test/", app=Quart(__name__))
