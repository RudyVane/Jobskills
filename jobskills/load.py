import os


def load_from_env() -> dict[str, str]:
    vars = dict(os.environ)
    to_load = [k for k in vars.keys() if k.endswith("_FILE")]
