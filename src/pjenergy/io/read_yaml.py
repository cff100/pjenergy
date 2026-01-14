from pathlib import Path
import yaml

def read_yaml(path: Path) -> dict:
    with open(path) as f:
        data = yaml.safe_load(f)

    return data