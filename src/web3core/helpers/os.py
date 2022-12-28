import json
import os
from typing import Any


def create_folder(dir: str, mode: int = 0o777) -> None:
    """Create a folder and all its parent folders, if they do not
    exist"""
    expanded_dir = os.path.expanduser(dir)
    if not os.path.isdir(expanded_dir):
        os.makedirs(expanded_dir, mode)
        os.chmod(expanded_dir, mode)  # for good measure


def read_json(file_path: str) -> Any:
    """Parse a JSON file in a python object"""
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)
