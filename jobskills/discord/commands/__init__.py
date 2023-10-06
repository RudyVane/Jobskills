import importlib

blueprints = [
    importlib.import_module(f".{name}", __name__).bp
    for name in ["ping", "offer", "modal", "help", "scrape"]
]
