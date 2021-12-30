"""Configurations."""
from enum import Enum
from pathlib import Path
import yaml

CONFIG_FILE = 'config.yaml'  # config file name
# file path from parent dir
CONFIG_FILE_PATH = Path(__file__).resolve().parent.parent.joinpath(CONFIG_FILE)

with open(CONFIG_FILE, 'r') as file:
    CONFIG = yaml.safe_load(file)


class Icons(Enum):
    """Emoji icons for todo status."""
    check = CONFIG['icons']['check']
    uncheck = CONFIG['icons']['uncheck']
