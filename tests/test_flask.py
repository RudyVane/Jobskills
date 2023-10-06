def test_flask_patch():
    import jobskills.flask  # isort:skip # noqa: F401
    from flask import request

    assert "quart.flask_patch" in type(request).__module__
