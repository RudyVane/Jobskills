def test_flask_patch():
    import jobskills.discord.flask  # isort:skip # noqa: F401
    from flask import request

    assert "quart_flask_patch" in type(request).__module__
