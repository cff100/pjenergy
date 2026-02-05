"""YAML read/write helpers."""

from pathlib import Path
import yaml

def read_yaml(path: Path) -> dict:
    """Read a YAML file and return its contents as a dictionary."""
    with open(path) as f:
        data = yaml.safe_load(f)

    return data


def write_yaml(data, path: Path):
    """Write raw data to a YAML file path."""
    with open(path, "w") as f:
        f.write(data)
