def test_validate():
    from jobskills.config import settings

    settings.validators.validate_all(exclude=["DISCORD"])
