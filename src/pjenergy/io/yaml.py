from pathlib import Path
import yaml

def read_yaml(path: Path) -> dict:
    with open(path) as f:
        data = yaml.safe_load(f)

    return data


def write_yaml(data, path: Path):
    with open(path, "w") as f:
        f.write(data)