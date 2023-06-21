from pathlib import Path
from typing import Any

import toml

config_file = "config.toml"


def load_config() -> Any:
    if not Path(config_file).exists():
        return {}
    with open(config_file) as f:
        config = toml.load(f)
        return config


def save_config(configuration) -> None:
    with open(config_file, "w") as f:
        toml.dump(configuration, f)
