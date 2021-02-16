import os
import pathlib

import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent

if os.environ.get("CONFIG_PATH"):
    config_path = BASE_DIR / os.environ["CONFIG_PATH"]
else:
    config_path = BASE_DIR / "config" / "config.yaml"


def get_config(path):
    with open(path) as f:
        parsed_config = yaml.safe_load(f)
    return parsed_config


config = get_config(config_path)
