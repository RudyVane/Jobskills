
from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    # environments=True,
    validators=[
        Validator("scraper.domains", must_exist=True, cast=dict),
        Validator("scraper.domains._default", must_exist=True),
        Validator("scraper.blacklists", must_exist=True)
    ],
    envvar_prefix="DYNACONF",
    settings_files=['settings.toml', '.secrets.toml'],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
