import importlib

blueprints = [
    importlib.import_module(f".{name}", __name__).bp
    for name in ["ping", "offer", "modal", "help", "scrape"]
]


def dump():
    return [
        command.dump() for bp in blueprints for command in bp.discord_commands.values()
    ]
