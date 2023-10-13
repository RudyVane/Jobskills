"""
Relies on the module loading system importing the parent modules
 before any of the submodules.
"""

import quart_flask_patch  # noqa: F401
from dynaconf import Validator

from ..config import settings

settings.validators.register(
    Validator("DISCORD_CLIENT_ID", must_exist=True),
    Validator("DISCORD_CLIENT_SECRET", must_exist=True),
    # 32-byte public key, 64 characters as hex
    Validator("DISCORD_PUBLIC_KEY", must_exist=True, len_eq=64),
    Validator("discord.testing_guild_id"),
    Validator("discord.endpoint"),
)
