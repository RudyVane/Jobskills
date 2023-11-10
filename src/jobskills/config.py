import os

from arq.connections import RedisSettings
from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    environments=True,
    validators=[
        Validator("scraper.domains", must_exist=True, cast=dict),
        Validator("scraper.domains._default", must_exist=True),
        Validator("scraper.blacklists", must_exist=True),
        Validator(
            "redis",
            must_exist=True,
            cast=lambda v: v
            if isinstance(v, RedisSettings)
            else RedisSettings.from_dsn(v),
        ),
        Validator("discord.msg_max_len", must_exist=True),
    ],
    envvar_prefix="JOBSKILLS",
    root_path=os.path.dirname(__file__),
    settings_files=["*.yml"],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
